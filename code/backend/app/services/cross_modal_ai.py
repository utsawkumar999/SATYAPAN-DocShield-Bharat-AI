import cv2
import numpy as np
import re
from typing import Dict, Any, Optional

class CrossModalAI:
    def verify_qr_and_ocr(self, image_bytes: Optional[bytes] = None, ocr_text: str = "") -> Dict[str, Any]:
        """
        Extracts QR code from document image and compares text against OCR extracted fields.
        Returns honest status: NO_QR_DETECTED if QR is absent, or actual overlap ratio.
        """
        if not image_bytes:
            return {
                "qr_detected": False,
                "qr_payload": None,
                "consistency_score": None,
                "status": "INCONCLUSIVE — No image data provided",
                "is_match": None
            }

        try:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {
                    "qr_detected": False,
                    "qr_payload": None,
                    "consistency_score": None,
                    "status": "INCONCLUSIVE — Invalid image format",
                    "is_match": None
                }

            detector = cv2.QRCodeDetector()
            qr_data, bbox, _ = detector.detectAndDecode(img)

            if qr_data:
                clean_qr = re.sub(r'[^a-zA-Z0-9\s]', '', qr_data).lower()
                clean_ocr = re.sub(r'[^a-zA-Z0-9\s]', '', ocr_text).lower()

                qr_words = set(clean_qr.split())
                ocr_words = set(clean_ocr.split())

                if qr_words and ocr_words:
                    common = qr_words.intersection(ocr_words)
                    match_ratio = len(common) / max(1, len(qr_words))
                else:
                    match_ratio = 0.0

                is_match = match_ratio > 0.4
                return {
                    "qr_detected": True,
                    "qr_payload": qr_data[:60] + "..." if len(qr_data) > 60 else qr_data,
                    "consistency_score": round(match_ratio * 100, 1),
                    "status": f"QR Code Detected ({round(match_ratio * 100, 1)}% OCR consistency)" if is_match else "QR Mismatch (OCR Data does not match QR Payload)",
                    "is_match": is_match
                }
            else:
                return {
                    "qr_detected": False,
                    "qr_payload": None,
                    "consistency_score": None,
                    "status": "NO_QR_DETECTED — Document contour does not contain a decodable QR code",
                    "is_match": None
                }
        except Exception as e:
            return {
                "qr_detected": False,
                "qr_payload": None,
                "consistency_score": None,
                "status": f"INCONCLUSIVE — QR decoding error: {str(e)}",
                "is_match": None
            }