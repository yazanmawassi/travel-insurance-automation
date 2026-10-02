import requests
from requests.auth import HTTPBasicAuth
from config import API_BASE_URL, API_USERNAME, API_PASSWORD


def save_insurance_policy(payload: dict):
    # Sendet die Vertragsdaten an die Insurance-Policy-API.
    response = requests.post(
        f"{API_BASE_URL}/insurance-policy",
        json=payload,
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )

    # Wirft eine Exception, falls der Request nicht erfolgreich war.
    response.raise_for_status()

    # Die API gibt die Versicherungsnummer als Text zurück.
    return response.text.strip().replace('"', "")


def print_documents(policy_id: str):
    # Sendet einen Druckauftrag für die Vertragsunterlagen.
    response = requests.post(
        f"{API_BASE_URL}/document/print-job/insurance-policy/{policy_id}",
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )

    return response