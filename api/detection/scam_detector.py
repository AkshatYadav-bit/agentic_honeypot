from typing import Dict


SCAM_KEYWORDS = {
    "urgency": ["urgent", "immediately", "asap", "now"],
    "account_threat": ["blocked", "suspended", "limited", "frozen"],
    "payment": ["pay", "payment", "upi", "bank", "transfer"],
    "authority": ["bank", "officer", "support", "kyc", "verification"],
    "credential": ["otp", "pin", "password"],
    "link": ["http", "www", ".com", ".in"]
}


class ScamDetector:
    def __init__(self):
        pass

    def analyze(self, message: str) -> Dict:
        """
        Analyze a single message and return signal scores.
        """
        text = message.lower()

        signals = {
            "urgency": 0,
            "account_threat": 0,
            "payment": 0,
            "authority": 0,
            "credential": 0,
            "link": 0
        }

        for category, keywords in SCAM_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    signals[category] = 1
                    break

        return signals
    
    def score(self, signals: Dict) -> float:
        """
        Convert signals into a scam probability score.
        """
        weights = {
            "urgency": 0.15,
            "account_threat": 0.2,
            "payment": 0.25,
            "authority": 0.15,
            "credential": 0.15,
            "link": 0.1
        }

        score = 0.0
        for k, v in signals.items():
            score += weights.get(k, 0) * v

        return min(score, 1.0)

