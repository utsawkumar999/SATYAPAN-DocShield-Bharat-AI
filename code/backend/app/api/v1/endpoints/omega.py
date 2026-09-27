from fastapi import APIRouter, File, UploadFile
from app.services.omega_orchestrator import OmegaOrchestrator
from app.services.evidence_fusion import EvidenceFusionEngine
from app.services.causal_ai import CausalAIEngine
from app.services.digital_trust_twin import DigitalTrustTwin
from app.services.red_team_simulator import RedTeamSimulator
from app.services.pdf_forensics import PDFForensicsEngine
from app.services.anti_spoofing import AntiSpoofingEngine
from app.services.tamper_sandbox import TamperSandboxEngine

router = APIRouter()

orchestrator = OmegaOrchestrator()
fusion_engine = EvidenceFusionEngine()
causal_engine = CausalAIEngine()
trust_twin = DigitalTrustTwin()
red_team = RedTeamSimulator()
pdf_forensics = PDFForensicsEngine()
anti_spoofing = AntiSpoofingEngine()
sandbox_engine = TamperSandboxEngine()

@router.post("/verify-omega")
async def verify_omega(file: UploadFile = File(...)):
    content = await file.read()
    file_name = file.filename
    
    orch_res = orchestrator.orchestrate(file_name)
    fusion_res = fusion_engine.fuse_evidence(content, file_name)
    causal_res = causal_engine.analyze_causal_risk(fusion_res["fused_risk_score"])
    trust_res = trust_twin.get_trust_profile("DS-" + file_name[:6].upper())
    red_res = red_team.run_robustness_tests()
    pdf_res = pdf_forensics.analyze_pdf_stream(content, file_name)
    
    return {
        "file_name": file_name,
        "digital_dna": fusion_res["digital_dna"],
        "risk_score": fusion_res["fused_risk_score"],
        "ela_score": fusion_res["ela_score"],
        "autonomous_orchestrator": orch_res,
        "evidence_fusion": fusion_res,
        "causal_ai": causal_res,
        "digital_trust_twin": trust_res,
        "red_team_simulation": red_res,
        "pdf_forensics": pdf_res
    }

from pydantic import BaseModel
import base64

class AntiSpoofRequest(BaseModel):
    frame_base64: str = None
    is_document_present: bool = True

@router.post("/anti-spoofing")
async def anti_spoofing_check(req: AntiSpoofRequest = None):
    frame_bytes = None
    is_doc = True if req is None else req.is_document_present
    if req and req.frame_base64:
        try:
            clean_b64 = req.frame_base64.split(",")[-1]
            frame_bytes = base64.b64decode(clean_b64)
        except Exception:
            frame_bytes = None
            
    return anti_spoofing.analyze_frame_liveness(frame_bytes=frame_bytes, is_document_present=is_doc)

@router.post("/simulate-tamper/{attack_type}")
async def simulate_tamper(attack_type: str):
    return sandbox_engine.simulate_attack(attack_type)
