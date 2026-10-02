import requests
from requests.auth import HTTPBasicAuth
from config import API_BASE_URL, API_USERNAME, API_PASSWORD
from utils import normalize


def search_partner_by_number(partnernummer: str):
    # Partner direkt über die Partnernummer suchen.
    response = requests.get(
        f"{API_BASE_URL}/partner/{partnernummer}",
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )

    # Wenn kein Partner gefunden wird, geben wir None zurück.
    if response.status_code == 404:
        return None

    # Bei anderen Fehlern soll Python eine Exception werfen.
    response.raise_for_status()

    # Antwort der API als Dictionary zurückgeben.
    return response.json()


def search_partner_by_data(policy_holder: dict):
    api_payload = {
        "firstName": normalize(policy_holder.get("firstname", "")),
        "lastName": normalize(policy_holder.get("lastname", "")),
        "birthDate": policy_holder.get("birthday", ""),
        "phoneNumber": policy_holder.get("phoneNumber", ""),
        "emailAddress": normalize(policy_holder.get("mail", ""))
    }

    address = policy_holder.get("address", {})
    if address:
        api_payload["address"] = {
            "street": address.get("street", ""),
            "number": address.get("number", ""),
            "postalCode": address.get("postCode", ""),
            "city": address.get("city", ""),
            "countryCode": address.get("country", "")
        }


    response = requests.post(
        f"{API_BASE_URL}/partner/search",
        json=api_payload,
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )


    if response.status_code == 404:
        return None

    if response.status_code >= 500:
        raise Exception(f"Partner API Fehler: {response.status_code} - {response.text}")

    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        if data:
            print("Partner gefunden:", data[0].get("partnerId"))
            return data[0]
        return None

    if isinstance(data, dict):
        if data.get("partnerId"):
            print("Partner gefunden:", data.get("partnerId"))
            return data
        return None

    return None


def create_partner(policy_holder: dict):
    # Neuen Partner aus den Daten des Versicherungsnehmers erstellen.
    api_payload = {
        "firstName": normalize(policy_holder.get("firstname", "")),
        "lastName": normalize(policy_holder.get("lastname", "")),
        "birthDate": policy_holder.get("birthday", ""),
        "phoneNumber": policy_holder.get("phoneNumber", ""),
        "emailAddress": normalize(policy_holder.get("mail", ""))
    }

    # Adresse aus dem Formular in das Format der API umwandeln.
    address = policy_holder.get("address", {})
    if address:
        api_payload["address"] = {
            "street": address.get("street", ""),
            "number": address.get("number", ""),
            "postalCode": address.get("postCode", ""),
            "city": address.get("city", ""),
            "countryCode": address.get("country", "")
        }

    # Neuen Partner in der API anlegen.
    response = requests.post(
        f"{API_BASE_URL}/partner",
        json=api_payload,
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )

    response.raise_for_status()

    # Die API gibt hier nur die Partner-ID als Text zurück.
    raw_response = response.text.strip().replace('"', "")

    if raw_response:
        print(f"Erfolgreich angelegt. Echte Partner-ID: {raw_response}")
        return {"partnerId": raw_response}

    return {"partnerId": ""}