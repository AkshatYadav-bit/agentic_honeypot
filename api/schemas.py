from pydantic import BaseModel
from typing import Dict, List, Any


class MessageRequest(BaseModel):
    session_id: str
    message: str


class IntelligenceItem(BaseModel):
    value: str
    confidence: float
    turn: int


class ExtractedIntelligence(BaseModel):
    upi_ids: List[IntelligenceItem]
    bank_accounts: List[IntelligenceItem]
    phishing_urls: List[IntelligenceItem]


class MetricsResponse(BaseModel):
    conversation_turns: int
    engagement_duration_sec: int
    dialogue_phase: str
    agent_active: bool
    intel_count: Dict[str, int]


class MessageResponse(BaseModel):
    scam_detected: bool
    scam_confidence: float
    reply: str
    metrics: MetricsResponse
    extracted_intelligence: ExtractedIntelligence
