# In dieser Datei stehen kleine Hilfsfunktionen,
# die an mehreren Stellen im Projekt benutzt werden.


def normalize(value):
    # Werte werden vereinheitlicht, damit der Vergleich nicht an Leerzeichen
    # oder Groß-/Kleinschreibung scheitert.
    return str(value or "").lower().replace(" ", "").strip()


def addresses_match(policy_holder: dict, partner: dict):
    # Adresse aus dem Antrag holen.
    input_address = policy_holder.get("address", {})

    # Adresse aus der Antwort der Partner-API holen.
    partner_address = partner.get("address", {})

    # Straße, Postleitzahl und Stadt werden verglichen.
    # Vor dem Vergleich werden die Werte normalisiert.
    return (
        normalize(input_address.get("street")) == normalize(partner_address.get("street"))
        and normalize(input_address.get("postCode")) == normalize(partner_address.get("postalCode"))
        and normalize(input_address.get("city")) == normalize(partner_address.get("city"))
    )