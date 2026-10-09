import re

class PDFForensicsEngine:
    def analyze_pdf_stream(self, pdf_bytes: bytes, file_name: str) -> dict:
        try:
            if not pdf_bytes.startswith(b'%PDF-'):
                return {
                    "file_name": file_name,
                    "is_pdf": False,
                    "pdf_version": "N/A",
                    "creator_software": "N/A",
                    "producer_software": "N/A",
                    "is_suspicious_software": False,
                    "integrity_verdict": "NOT_A_PDF — File is not in valid PDF format"
                }

            content_str = pdf_bytes.decode('latin1', errors='ignore')
            
            # Extract PDF version
            version_match = re.search(r'%PDF-(\d+\.\d+)', content_str)
            pdf_version = f"PDF {version_match.group(1)}" if version_match else "PDF (Unknown Version)"

            # Extract metadata tags
            creator_match = re.search(r'/Creator\s*\((.*?)\)', content_str)
            producer_match = re.search(r'/Producer\s*\((.*?)\)', content_str)
            
            creator = creator_match.group(1) if creator_match else "Unspecified / Stripped"
            producer = producer_match.group(1) if producer_match else "Unspecified / Stripped"
            
            suspicious_tools = ["photoshop", "canva", "gimp", "illustrator", "word", "paint", "corel", "acrobat distiller"]
            combined_meta = (creator + " " + producer).lower()
            is_suspicious = any(soft in combined_meta for soft in suspicious_tools)
            
            # Check for digital signature dictionary (/ByteRange, /Contents, /SubFilter)
            has_digital_signature = bool(re.search(r'/ByteRange\s*\[', content_str) and re.search(r'/SubFilter\s*/adbe\.pkcs7', content_str))

            if is_suspicious:
                verdict = "SUSPICIOUS PDF — Editing/design software metadata detected"
            elif has_digital_signature:
                verdict = "DIGITALLY SIGNED PDF — Embedded PKCS#7 signature stream found"
            else:
                verdict = "STANDARD PDF — Clean metadata (No embedded signature detected; subject to e-KYC)"

            return {
                "file_name": file_name,
                "is_pdf": True,
                "pdf_version": pdf_version,
                "creator_software": creator,
                "producer_software": producer,
                "is_suspicious_software": is_suspicious,
                "has_digital_signature": has_digital_signature,
                "integrity_verdict": verdict
            }
        except Exception as e:
            return {
                "file_name": file_name,
                "is_pdf": False,
                "pdf_version": "N/A",
                "creator_software": "N/A",
                "producer_software": "N/A",
                "is_suspicious_software": False,
                "integrity_verdict": f"INCONCLUSIVE — PDF forensic error: {str(e)}"
            }
