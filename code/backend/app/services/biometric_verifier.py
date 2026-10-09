import cv2
import numpy as np
from typing import Dict, Any, Optional

class BiometricVerifier:
    def verify_faces(self, doc_image_bytes: Optional[bytes] = None, selfie_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Face verification module:
        - Detects faces in document image and live selfie
        - Computes cosine similarity of normalized image arrays
        - Never fabricates match percentages when input is missing
        """
        if not doc_image_bytes or not selfie_bytes:
            return {
                "face_crop_detected": False,
                "selfie_provided": bool(selfie_bytes),
                "match_score": None,
                "status": "INCONCLUSIVE — Verification selfie not provided",
                "is_match": None
            }

        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)

            doc_img = cv2.imdecode(np.frombuffer(doc_image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
            selfie_img = cv2.imdecode(np.frombuffer(selfie_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)

            if doc_img is None or selfie_img is None:
                return {
                    "face_crop_detected": False,
                    "selfie_provided": True,
                    "match_score": None,
                    "status": "INCONCLUSIVE — Image decoding failed",
                    "is_match": False
                }

            doc_faces = face_cascade.detectMultiScale(doc_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            selfie_faces = face_cascade.detectMultiScale(selfie_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(doc_faces) > 0 and len(selfie_faces) > 0:
                x1, y1, w1, h1 = doc_faces[0]
                x2, y2, w2, h2 = selfie_faces[0]

                face1 = cv2.resize(doc_img[y1:y1+h1, x1:x1+w1], (64, 64)).flatten().astype(np.float32)
                face2 = cv2.resize(selfie_img[y2:y2+h2, x2:x2+w2], (64, 64)).flatten().astype(np.float32)

                norm1 = np.linalg.norm(face1)
                norm2 = np.linalg.norm(face2)
                
                if norm1 > 0 and norm2 > 0:
                    similarity = float(np.dot(face1, face2) / (norm1 * norm2))
                    match_score = round(max(0.0, min(100.0, similarity * 100.0)), 1)
                else:
                    match_score = 0.0

                is_match = match_score > 65.0
                return {
                    "face_crop_detected": True,
                    "selfie_provided": True,
                    "match_score": match_score,
                    "status": f"{match_score}% Face Similarity Match" if is_match else f"{match_score}% Similarity (Mismatch Detected)",
                    "is_match": is_match
                }
            else:
                return {
                    "face_crop_detected": len(doc_faces) > 0,
                    "selfie_provided": True,
                    "match_score": None,
                    "status": "INCONCLUSIVE — Face could not be detected in both images",
                    "is_match": False
                }
        except Exception as e:
            return {
                "face_crop_detected": False,
                "selfie_provided": True,
                "match_score": None,
                "status": f"INCONCLUSIVE — Face analysis error: {str(e)}",
                "is_match": False
            }
