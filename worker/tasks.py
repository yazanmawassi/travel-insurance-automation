from datetime import date

from partner_api import (
    search_partner_by_number,
    search_partner_by_data,
    create_partner
)
from insurance_api import save_insurance_policy, print_documents
from utils import addresses_match, normalize


def register_tasks(worker):
    # In dieser Funktion werden alle Camunda Service Tasks registriert.

    @worker.task(task_type="validate-data")
    def validate_data(travelInsurance: dict):
        print("Daten validieren...")

        # Reisedaten aus den Prozessvariablen holen.
        travel_data = travelInsurance.get("travelData", {})

        # Werte für die Validierung vorbereiten.
        beginn = date.fromisoformat(travel_data.get("start"))
        ende = date.fromisoformat(travel_data.get("end"))
        kosten = float(travel_data.get("cost", 0))

        # Ergebnisse werden an Camunda zurückgegeben und können im Gateway benutzt werden.
        return {
            "datenGueltig": beginn < ende and beginn > date.today() and kosten > 0,
            "reisebeginnVorReiseende": beginn < ende,
            "reisebeginnInZukunft": beginn > date.today(),
            "reisekostenPositiv": kosten > 0
        }

    @worker.task(task_type="search-vn")
    def search_vn(travelInsurance: dict):
        print("VN im Partnersystem suchen...")

        # Versicherungsnehmer aus dem Antrag lesen.
        policy_holder = travelInsurance.get("policyHolder", {})

        # Prüfen, ob schon eine Partnernummer angegeben wurde.
        partnernummer = policy_holder.get("id", "")

        if not partnernummer:
            return {"partnernummerAngegeben": False}

        try:
            # Partner mit der angegebenen Partnernummer suchen.
            partner = search_partner_by_number(partnernummer)

            if partner is None:
                return {
                    "partnernummerAngegeben": True,
                    "partnerMitPartnernummerGefunden": False
                }

            # Adresse aus Antrag und Partnersystem vergleichen.
            adresse_stimmt = addresses_match(policy_holder, partner)

            return {
                "partnernummerAngegeben": True,
                "partnerMitPartnernummerGefunden": True,
                "partnernummer": partner.get("partnerId", partnernummer),
                "partnerAusApi": partner,
                "adresseStimmtUeberein": adresse_stimmt
            }

        except Exception as e:
            # Bei technischen Fehlern wird apiFehler gesetzt.
            print("Fehler bei search-vn:", e)
            return {
                "partnernummerAngegeben": True,
                "partnerMitPartnernummerGefunden": False,
                "apiFehler": True
            }

    @worker.task(task_type="search-partner")
    def search_partner(travelInsurance: dict):
        print("Partner im System suchen...")

        try:
            # Suche ohne Partnernummer, also über die persönlichen Daten.
            partner = search_partner_by_data(travelInsurance.get("policyHolder", {}))

            if partner is None:
                return {"partnerPerSucheGefunden": False}

            return {
                "partnerPerSucheGefunden": True,
                "partnernummer": partner.get("partnerId"),
                "partnerAusApi": partner
            }

        except Exception as e:
            print("Fehler bei search-partner:", e)
            return {
                "partnerPerSucheGefunden": False,
                "apiFehler": True,
                "fehlermeldung": str(e)
            }

    @worker.task(task_type="create-partner")
    def create_partner_task(travelInsurance: dict):
        print("Neukunde im System anlegen...")

        try:
            # Falls kein Partner gefunden wurde, wird ein neuer Partner angelegt.
            partner = create_partner(travelInsurance.get("policyHolder", {}))
            new_partner_id = partner.get("partnerId", "")

            # Die neue Partnernummer wird auch im travelInsurance-Objekt gespeichert.
            if "policyHolder" not in travelInsurance:
                travelInsurance["policyHolder"] = {}

            travelInsurance["policyHolder"]["id"] = new_partner_id


            return {
                "partnernummer": new_partner_id,
                "partnerAusApi": partner,
                "neukundeAngelegt": True,
                "travelInsurance": travelInsurance
            }

        except Exception as e:
            print("Fehler bei create-partner:", e)
            return {
                "neukundeAngelegt": False,
                "apiFehler": True
            }

    @worker.task(task_type="vertrag-speichern")
    def vertrag_speichern(travelInsurance: dict, partnernummer: str = "", Selbstbehalt: int = 0):
        print("Vertrag speichern in API...")

        # Für den Vertrag brauchen wir eine gültige Partnernummer.
        p_id = partnernummer

        if not p_id:
            p_id = travelInsurance.get("policyHolder", {}).get("id", "")

        if not p_id:
            return {
                "apiFehler": True,
                "vertragGespeichert": False,
                "fehlermeldung": "Keine Partnernummer gefunden"
            }

        # Reisedaten aus den Prozessvariablen holen.
        travel_data = travelInsurance.get("travelData", {})

        # Versicherte Personen auslesen.
        insured_persons_input = travelInsurance.get("insuredPartners", [])

        # Versicherte Personen in das Format der API umwandeln.
        insured_persons = []
        for person in insured_persons_input:
            insured_persons.append({
                "firstName": normalize(person.get("firstname", "")),
                "lastName": normalize(person.get("lastname", "")),
                "birthDate": person.get("birthday", ""),
                "childOfInsuranceTaker": person.get("childOfPolicyHolder", False)
            })

        # Payload für die Insurance-Policy-API zusammenbauen.
        payload = {
            "insuranceTakerId": p_id,
            "travelDetails": {
                "begin": travel_data.get("start", ""),
                "end": travel_data.get("end", ""),
                "destinationCountryCode": travel_data.get("destination", ""),
                "totalCost": int(float(travel_data.get("cost", 0))),
                "currency": travel_data.get("currency", "EUR")
            },
            "coverage": {
                "costRetention": Selbstbehalt,
                "withBaggageCoverage": travelInsurance.get("baggageInsurance", False),
                "withTravelAbortionCoverage": travelInsurance.get("travelCancellation", False),
                "withTravelExtensionCoverage": False
            },
            "insuredPersons": insured_persons
        }

        try:

            # Vertrag speichern und Versicherungsnummer zurückbekommen.
            versicherungsnummer = save_insurance_policy(payload)

            return {
                "versicherungsnummer": versicherungsnummer,
                "vertragGespeichert": True,
                "apiFehler": False
            }

        except Exception as e:
            print("Fehler beim Speichern des Vertrags:", e)
            return {
                "apiFehler": True,
                "vertragGespeichert": False,
                "fehlermeldung": str(e)
            }

    @worker.task(task_type="unterlagen-drucken")
    def unterlagen_drucken(versicherungsnummer: str = "V-UNBEKANNT"):
        print(f"Vertragsunterlagen für Vertrag {versicherungsnummer} drucken...")

        try:
            # Die Versicherungsnummer wird an die Dokumenten-API übergeben.
            response = print_documents(versicherungsnummer)

            # Laut Swagger bedeutet 202, dass der Druckauftrag angenommen wurde.
            if response.status_code == 202:
                return {"unterlagenGedruckt": True}

            # Wenn die Police nicht gefunden wurde.
            if response.status_code == 404:
                return {
                    "unterlagenGedruckt": False,
                    "printWarnung": "Versicherungspolice wurde nicht gefunden"
                }

            response.raise_for_status()

            return {"unterlagenGedruckt": True}

        except Exception as e:
            print("Fehler beim Drucken:", e)
            return {
                "unterlagenGedruckt": False,
                "printWarnung": str(e)
            }