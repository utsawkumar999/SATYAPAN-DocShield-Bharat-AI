class WhatIfSimulator:
    @staticmethod
    def simulate_whatif(base_case: dict, ignore_qr: bool = False, ignore_tampering: bool = False) -> dict:
        score = base_case.get("risk_score", 85)
        if ignore_qr:
            score -= 25
        if ignore_tampering:
            score -= 30
        return {
            "original_score": base_case.get("risk_score", 85),
            "simulated_score": max(0, score)
        }
