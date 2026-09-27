import easyocr
import os

class HybridOCREngine:
    def __init__(self):
        self.reader = easyocr.Reader(("en", "hi"), gpu=False)
    def process_document(self, path):
        return {"status": "OCR_PROCESSED"}