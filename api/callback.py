import requests
import logging

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_result(session):
    """
    Sends final extracted intelligence to GUVI evaluation endpoint.
    """

    extracted = session.extracted_intelligence or {}

    # ---- Build extracted intelligence EXACTLY as GUVI expects ----
    payload = {
        "sessionId": session.session_id,
        "scamDetected": True,  # must be true when callback is sent
        "totalMessagesExchanged": session.turn_count,
        "extractedIntelligence": {
            "bankAccounts": [b.get("value") for b in extracted.get("bank_accounts", [])],
            "upiIds": [u.get("value") for u in extracted.get("upi_ids", [])],
            "phishingLinks": [p.get("value") for p in extracted.get("phishing_urls", [])],
            "phoneNumbers": extracted.get("phone_numbers", []),
            "suspiciousKeywords": extracted.get("suspicious_keywords", [])
        },
        "agentNotes": _generate_agent_notes(session)
    }

    try:
        response = requests.post(
        GUVI_CALLBACK_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10,
        verify=True
        )

        print("CALLBACK STATUS =", response.status_code)
        print("CALLBACK RESPONSE =", response.text)

        logging.info(
            f"GUVI CALLBACK | status={response.status_code} | response={response.text}"
        )

        return response.status_code == 200

    except Exception as e:
        logging.error(f"GUVI CALLBACK FAILED: {str(e)}")
        return False


def _generate_agent_notes(session):
    notes = []

    if session.scam_confidence >= 0.7:
        notes.append("High confidence scam detected")

    if session.extracted_intelligence.get("upi_ids"):
        notes.append("Payment redirection via UPI")

    if session.extracted_intelligence.get("bank_accounts"):
        notes.append("Bank account details shared")

    if session.extracted_intelligence.get("phishing_urls"):
        notes.append("Phishing links shared")

    return "; ".join(notes) if notes else "Scam engagement completed successfully"
