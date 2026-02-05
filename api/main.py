from fastapi import FastAPI, Depends
from api.session_store import SessionStore
from api.detection.scam_detector import ScamDetector
from api.agent.orchestrator import AgentOrchestrator
from api.extraction.intelligence import IntelligenceExtractor
from api.auth import verify_api_key
from api.metrics import MetricsEngine
from api.schemas import MessageRequest, MessageResponse

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

    if session.scam_confidence >= 0.6:
        session.agent_active = True
        if session.dialogue_phase == "pre_detection":
            session.dialogue_phase = "engagement"

    # ---- Agent decision & reply ----
    agent_result = agent.handle(session)
    reply_text = agent_result["reply"]

    session.add_message("agent", reply_text)

    # ---- Intelligence extraction ----
    extracted = extractor.extract(data.message)
    extractor.merge_into_session(session, extracted)

    # ---- Metrics ----
    metrics = metrics_engine.update(session)

    # ---- Final Response ----
    return {
        "scam_detected": session.agent_active,
        "scam_confidence": round(session.scam_confidence, 2),
        "reply": reply_text,
        "metrics": metrics,
        "extracted_intelligence": session.extracted_intelligence
    }
