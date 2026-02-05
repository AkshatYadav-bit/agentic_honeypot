import requests


GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


def send_final_result(session):
    """
    Sends final extracted intelligence to GUVI evaluation endpoint.
    """

    extracted = session.extracted_intelligence

    payload = {
        "sessionId": session.session_id,
        "scamDetected": session.agent_active,
        "totalMessagesExchanged": session.turn_count,
        "extractedIntelligence": {
            "bankAccounts": [b["value"] for b in extracted["bank_accounts"]],
            "upiIds": [u["value"] for u in extracted["upi_ids"]],
            "phishingLinks": [p["value"] for p in extracted["phishing_urls"]],
            "phoneNumbers": [],  # optional, add later if you extract
            "suspiciousKeywords": []  # optional
        },
        "agentNotes": _generate_agent_notes(session)
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print("GUVI callback failed:", e)
        return False


def _generate_agent_notes(session):
    notes = []

    if session.scam_confidence > 0.7:
        notes.append("High confidence scam detected")

    if len(session.extracted_intelligence["upi_ids"]) > 0:
        notes.append("Payment redirection via UPI")

    if len(session.extracted_intelligence["phishing_urls"]) > 0:
        notes.append("Phishing links shared")

    return "; ".join(notes) if notes else "Scam engagement completed"
