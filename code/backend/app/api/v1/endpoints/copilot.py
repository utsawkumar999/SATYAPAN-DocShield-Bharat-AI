from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
class CopilotQuery(BaseModel):
    case_id: str
    question: str

@router.post("/copilot/chat")
async def copilot_chat(query: CopilotQuery):
    return {
        "case_id": query.case_id,
        "question": query.question,
        "answer": f"DocShield AI X Copilot: Case that was analyzed.",
        "status": "COPILOT_RESPONSE_READN"
    }
