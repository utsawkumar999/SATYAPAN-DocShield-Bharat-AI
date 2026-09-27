from fastapi import APIRouter
from app.api.v1.endpoints import verify, copilot, omega, bharat

api_router = APIRouter()
api_router.include_router(verify.router, prefix="", tags=["verification"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
api_router.include_router(omega.router, prefix="/omega", tags=["omega"])
api_router.include_router(bharat.router, prefix="/bharat", tags=["bharat"])
