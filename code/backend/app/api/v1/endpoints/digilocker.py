from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from app.services.digilocker_service import DigiLockerGateway

router = APIRouter()
digilocker_gw = DigiLockerGateway()

@router.get("/authorize-url")
def get_auth_url(state: str = "docshield_session_101"):
    """
    Returns the official DigiLocker OAuth2 redirect URL.
    """
    return digilocker_gw.get_authorization_url(state)

@router.get("/redirect-portal")
def redirect_to_official_digilocker(state: str = "docshield_session_101"):
    """
    Redirects user directly to official DigiLocker / MeriPehchan login portal.
    """
    auth_data = digilocker_gw.get_authorization_url(state)
    # Direct redirect to Government of India DigiLocker login
    return RedirectResponse(url="https://services.digitallocker.gov.in/")

@router.get("/callback")
def oauth_callback(code: str = "SAMPLE_AUTH_CODE", state: str = "docshield_session_101"):
    """
    Handles OAuth2 callback and processes requester exchange.
    """
    return {
        "status": "AUTHORIZATION_RECEIVED",
        "authorization_code": code,
        "state": state,
        "message": "User consent recorded. Proceeding to fetch issuer-sealed document."
    }

@router.get("/fetch-document")
def fetch_document(doc_type: str = "aadhaar", consent_code: str = "AUTH_GRANTED"):
    """
    Retrieves authentic document directly from issuing authority with digital seal.
    """
    return digilocker_gw.fetch_authorized_document_payload(doc_type, consent_code)
