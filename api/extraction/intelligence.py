import re
from typing import Dict, List


UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
BANK_ACCOUNT_REGEX = r"\b\d{9,18}\b"
URL_REGEX = r"https?://[^\s]+"


class IntelligenceExtractor:
    def extract(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract raw intelligence from text.
        """
        upis = re.findall(UPI_REGEX, text)
        banks = re.findall(BANK_ACCOUNT_REGEX, text)
        urls = re.findall(URL_REGEX, text)

        results = {
            "upi_ids": [
                {"value": u, "confidence": 0.85} for u in upis
            ],
            "bank_accounts": [
                {"value": b, "confidence": 0.8} for b in banks
            ],
            "phishing_urls": [
                {"value": url, "confidence": 0.9} for url in urls
            ]
        }

        return results

    def merge_into_session(self, session, extracted: Dict):
        """
        Deduplicate and store intelligence into session state.
        """
        for key in session.extracted_intelligence.keys():
            existing_values = {
                item["value"] for item in session.extracted_intelligence[key]
            }

            for item in extracted.get(key, []):
                if item["value"] not in existing_values:
                    session.extracted_intelligence[key].append({
                        "value": item["value"],
                        "confidence": item["confidence"],
                        "turn": session.turn_count
                    })
