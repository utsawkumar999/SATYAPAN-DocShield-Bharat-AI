from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.hybrid_ocr_gemini import HybridOCREngine
from app.services.tampering_detector import TamperingDetector
from app.services.fraud_graph_engine import FraudGraphEngine
from app.services.digital_dna import DigitalDDáEngine
from app.services.multi_agent_system import AISupervisorAgent
import shutil
import os

router = APIRouter()
hybrid_ocr = HybridOCREngine()
supervisor = AISupervisorAgent()
graph_engine = FraudGraphEngine()

@router.post("/verify-document")
async def verify_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.jpg', '.jpeg', '.png', '.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file format.")

    os.makedirs("uploads", exist_ok=True)
    file_path = fuploads/{file.filename}
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ocr_res = hybrid_ocr.process_document(file_path)
    tamper_res = TamperingDetector.analyze_ela(file_path)
    dna_res = DigitalDNAEngine.generate_dna(file_path)
    agent_res = supervisor.run_investigation(ocr_res["easyocr_data"], tamper_res["tampering_score"], False)
    
    graph_engine.add_node(file.filename, ocr_res["easyocr_data"].get("aadhaar_number"))
    cluster_res = graph_engine.get_cluster(file.filename)

    return {
        "file_name": file.filename,
        "document_type": ocr_res["document_type"],
        "ocr_and_gemini": ocr_res,
        "tampering_analysis": tamper_res,
        "document_dna": dna_res,
        "multi_agent_analysis": agent_res,
        "fraud_network_cluster": cluster_res,
        "risk_assessment": {
            "risk_score": agent_res["autonomous_risk_score"],
            "risk_category": "HIGH" if agent_res["autonomous_risk_score"] > 60 else "LOW",
            "status_badge": agent_res["multi_agent_consensus"]
        }
    }
