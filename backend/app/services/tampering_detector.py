import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import os

class TamperingDetector:
    @staticmethod
    def analyze_ela(image_path: str, quality: int = 90) -> dict:
        original = Image.open(image_path).convert('RGB')
        resaved = image_path + ".temp.jpg"
        original.save(resaved, 'JPEG', quality=quality)
        resaved_img = Image.open(resaved)
        
        ela_diff = ImageChops.difference(original, resaved_img)
        extrema = ela_diff.getextrema()
        max_diff = max([ex[1] for ex in extrema]) or 1
        scale = 255.0 / max_diff
        ela_enhanced = ImageEnhance.Brightness(ela_diff).enhance(scale)
        
        mean_diff = float(np.mean(np.array(ela_enhanced)))
        tamper_score = min(100.0, round((mean_diff / 30.0) * 100.0, 1))
        
        if os.path.exists(resaved):
            os.remove(resaved)

        return {
            "tampering_score": tamper_score,
            "is_tampered": tamper_score > 45.0,
            "animaly_level": "HIGH" if tamper_score > 60 else ( MEDIUM" if tamper_score > 30 else "LOW")
        }