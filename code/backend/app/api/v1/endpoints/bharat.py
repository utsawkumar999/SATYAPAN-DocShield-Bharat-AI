from fastapi import APIRouter
from app.services.bharat_engine import DocShieldBharatEngine
from pydantic import BaseModel

router = APIRouter()
bharat_engine = DocShieldBharatEngine()

class NoteRequest(BaseModel):
    reviewer: str
    note: str

@router.get("/status")
def get_bharat_status():
    return bharat_engine.get_system_status()

@router.post("/priority-queue/{case_id}")
def process_priority(case_id: str, is_emergency: bool = False):
    return bharat_engine.process_priority_case(case_id, is_emergency)

@router.post("/collaboration-note")
def add_note(req: NoteRequest):
    return bharat_engine.add_investigator_note(req.reviewer, req.note)

@router.get("/multilingual-insight/{lang}")
def get_multilingual_insight(lang: str):
    return bharat_engine.get_multilingual_insights(lang)

@router.get("/uidai-verify/{aadhaar_num}")
def verify_aadhaar_uidai(aadhaar_num: str):
    return bharat_engine.verify_aadhaar_uidai(aadhaar_num)
