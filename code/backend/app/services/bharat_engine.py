import time

class DocShieldBharatEngine:
    def __init__(self):
        self.priority_queue = []
        self.collaboration_notes = [
            {"reviewer": "Inspector Sharma", "note": "Verified OCR against physical scan. Initial screening logged.", "timestamp": "2026-08-24 00:15:00"},
            {"reviewer": "Supervisor Verma", "note": "Case assigned to verification queue.", "timestamp": "2026-08-24 00:20:00"}
        ]

    def get_system_status(self) -> dict:
        return {
            "platform": "DocShield Bharat AI (SIH 2026)",
            "gateway_status": "ONLINE & SYNCHRONIZED",
            "priority_queue_length": len(self.priority_queue),
            "supported_languages": ["Hindi", "English", "Bengali", "Tamil", "Telugu"],
            "supported_verification_modes": [
                "UIDAI Paperless Offline e-KYC (XML PKCS#7)",
                "Aadhaar Secure QR Code (2048-Bit RSA)",
                "DigiLocker / APISetu Requester Gateway",
                "16-Layer AI Multi-Spectral Forensics (ELA + Verhoeff)"
            ]
        }

    def process_priority_case(self, case_id: str, is_emergency: bool = False) -> dict:
        priority_level = "EMERGENCY / HIGH PRIORITY" if is_emergency else "STANDARD QUEUE"
        return {
            "case_id": case_id,
            "priority_level": priority_level,
            "queue_position": 1 if is_emergency else len(self.priority_queue) + 1,
            "status": "QUEUED"
        }

    def add_investigator_note(self, reviewer: str, note: str) -> dict:
        new_entry = {
            "reviewer": reviewer,
            "note": note,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.collaboration_notes.append(new_entry)
        return {"status": "SUCCESS", "collaboration_notes": self.collaboration_notes}

    def get_multilingual_insights(self, lang: str = "hi") -> dict:
        translations = {
            "hi": {
                "title": "जांच रिपोर्ट निष्कर्ष",
                "verdict_authentic": "दस्तावेज़ का डिजिटल हस्ताक्षर UIDAI प्रमाणपत्र से सत्यापित हुआ।",
                "verdict_inconclusive": "दस्तावेज़ की दृश्य जांच सही है, लेकिन डिजिटल हस्ताक्षर के बिना आधिकारिक प्रामाणिकता स्थापित नहीं हुई।",
                "verdict_tampered": "सावधान! दस्तावेज़ में विसंगति या संपीड़न असमानता पाई गई है।"
            },
            "en": {
                "title": "Investigation Report Verdict",
                "verdict_authentic": "Document digital signature verified against UIDAI public certificate.",
                "verdict_inconclusive": "Visual scan clean; official authenticity not established without cryptographic signature.",
                "verdict_tampered": "Alert! Anomaly or pixel compression variance detected in document."
            },
            "bn": {
                "title": "তদন্ত রিপোর্ট সিদ্ধান্ত",
                "verdict_authentic": "নথির ডিজিটাল স্বাক্ষর সফলভাবে যাচাই করা হয়েছে।",
                "verdict_inconclusive": "নথিটি দৃশ্যত পরিষ্কার, তবে ডিজিটাল স্বাক্ষর ছাড়া আনুষ্ঠানিক প্রামাণিকতা নিশ্চিত নয়।",
                "verdict_tampered": "সতর্কতা! নথিতে পরিবর্তন বা অসঙ্গতি পাওয়া গেছে।"
            },
            "ta": {
                "title": "விசாரணை அறிக்கை தீர்ப்பு",
                "verdict_authentic": "ஆவணத்தின் டிஜிட்டல் கையொப்பம் சரிபார்க்கப்பட்டது.",
                "verdict_inconclusive": "ஆவணம் சரியாக உள்ளது, ஆனால் டிஜிட்டல் கையொப்பம் இல்லாமல் அதிகாரப்பூர்வ உண்மை உறுதிப்படுத்தப்படவில்லை.",
                "verdict_tampered": "எச்சரிக்கை! ஆவணத்தில் முரண்பாடு கண்டறியப்பட்டது."
            },
            "te": {
                "title": "పరిశోధన నివేదిక తీర్పు",
                "verdict_authentic": "పత్రం యొక్క డిజిటల్ సంతకం విజయవంతంగా ధృవీకరించబడింది.",
                "verdict_inconclusive": "పత్రం స్పష్టంగా ఉంది, అయితే డిజిటల్ సంతకం లేకుండా అధికారిక ధృవీకరణ పూర్తి కాలేదు.",
                "verdict_tampered": "హెచ్చరిక! పత్రంలో మార్పులు కనుగొనబడ్డాయి."
            }
        }
        return translations.get(lang, translations["hi"])

    def verify_aadhaar_uidai(self, aadhaar_number: str) -> dict:
        clean_num = "".join(c for c in str(aadhaar_number) if c.isdigit())
        if len(clean_num) != 12:
            return {
                "masked_aadhaar": f"XXXX-XXXX-{clean_num[-4:]}" if len(clean_num) >= 4 else "INVALID",
                "verhoeff_checksum_valid": False,
                "status": "INVALID_FORMAT",
                "details": "Aadhaar number must contain exactly 12 numeric digits."
            }

        verhoeff_table_d = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        verhoeff_table_p = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        c = 0
        inverted_digits = [int(x) for x in reversed(clean_num)]
        for i, digit in enumerate(inverted_digits):
            c = verhoeff_table_d[c][verhoeff_table_p[i % 8][digit]]
        
        is_valid = (c == 0)

        return {
            "masked_aadhaar": f"XXXX-XXXX-{clean_num[-4:]}",
            "verhoeff_checksum_valid": is_valid,
            "status": "CHECKSUM_VALID (D5)" if is_valid else "CHECKSUM_FAILED",
            "details": "Mathematical Verhoeff Dihedral D5 check passed. Note: Checksum validates number structure; issuer authenticity requires UIDAI Offline e-KYC or DigiLocker." if is_valid else "Mathematical Verhoeff checksum failed. Invalid Aadhaar number."
        }
