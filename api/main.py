from fastapi import FastAPI, Depends
from api.session_store import SessionStore
from api.detection.scam_detector import ScamDetector
from api.agent.orchestrator import AgentOrchestrator
from api.extraction.intelligence import IntelligenceExtractor
from api.auth import verify_api_key
from api.metrics import MetricsEngine
from api.schemas import MessageRequest, MessageResponse
from api.callback import send_final_result


# --------------------
# App Initialization
# --------------------

app = FastAPI()

session_store = SessionStore()
detector = ScamDetector()
agent = AgentOrchestrator()
extractor = IntelligenceExtractor()
metrics_engine = MetricsEngine()

# --------------------
# Health Check
# --------------------

@app.get("/")
def health():
    return {"status": "alive"}

# --------------------
# Main Message Endpoint
# --------------------
@app.post("/message", response_model=MessageResponse)
def handle_message(
    data: MessageRequest,
    _: str = Depends(verify_api_key)
):
    # ---- Session ----
    session = session_store.get_or_create(data.session_id)

    # ---- Store incoming scammer message ----
    session.add_message("scammer", data.message)

    # ---- Scam detection ----
    signals = detector.analyze(data.message)
    score = detector.score(signals)
    session.scam_confidence = max(session.scam_confidence, score)

    # ---- Intelligence extraction ----
    extracted = extractor.extract(data.message)
    extractor.merge_into_session(session, extracted)

    # ---- Escalate scam confidence based on extracted intelligence ----
    if extracted["upi_ids"]:
        session.scam_confidence = max(session.scam_confidence, 0.8)

    if extracted["bank_accounts"]:
        session.scam_confidence = max(session.scam_confidence, 0.9)

    if extracted["phishing_urls"]:
        session.scam_confidence = max(session.scam_confidence, 0.95)

    # ---- Activate agent if scam confirmed ----
    if session.scam_confidence >= 0.6:
        session.agent_active = True
        if session.dialogue_phase == "pre_detection":
            session.dialogue_phase = "engagement"

    # ---- Dialogue phase progression (authoritative state machine) ----
    if session.agent_active:
        if session.dialogue_phase == "engagement":
            session.dialogue_phase = "payment_induction"

        if (
            session.dialogue_phase == "payment_induction"
            and (
                session.extracted_intelligence["upi_ids"]
                or session.extracted_intelligence["bank_accounts"]
                or session.extracted_intelligence["phishing_urls"]
            )
        ):
            session.dialogue_phase = "confirmation"

    # ---- Behavioral adaptation ----
    if session.turn_count > 5 and session.agent_active:
        session.trust_level = min(session.trust_level + 0.1, 1.0)

    # ---- Agent decision & reply (AFTER state is correct) ----
    agent_result = agent.handle(session)
    reply_text = agent_result["reply"]
    session.add_message("agent", reply_text)

    # ---- Metrics ----
    metrics = metrics_engine.update(session)

    # ---- Final GUVI callback ----
    if (
        session.agent_active
        and session.dialogue_phase == "confirmation"
        and session.turn_count >= 6
        and not session.final_callback_sent
    ):
        success = send_final_result(session)
        if success:
            session.final_callback_sent = True
            print("Final callback triggered for session:", session.session_id)

    # ---- Final Response ----
    return {
        "scam_detected": session.agent_active,
        "scam_confidence": round(session.scam_confidence, 2),
        "reply": reply_text,
        "metrics": metrics,
        "extracted_intelligence": session.extracted_intelligence
    }
