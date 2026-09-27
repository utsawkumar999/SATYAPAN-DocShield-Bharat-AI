from fastapi import APIRouter
from app.api.v1.endpoints import verify, copilot

api_router = APIRouter()
api_router.include_router(verify.router, prefix="", tags=["Verification"])
api_router.include_router(copilot.router, prefix="", tags=["Copilot"])
