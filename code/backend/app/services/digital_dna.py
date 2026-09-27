import hashlib
import time

class DigitalDNAEngine:
    def generate_dna(self, file_bytes: bytes, file_name: str) -> dict:
        sha256 = hashlib.sha256(file_bytes).hexdigest().upper()
        dna_hash = f"DNA-{sha256[:6]}-{sha256[6:10]}-{sha256[10:14]}"
        ledger_signature = f"DS-PROOF-{sha256[14:30]}"
        
        return {
            "digital_dna": dna_hash,
            "ledger_signature": ledger_signature,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_hash": sha256
        }