from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union


class NestedMessage(BaseModel):
    sender: Optional[str] = "scammer"
    text: str
    timestamp: Optional[int] = None


class HistoryMessage(BaseModel):
    sender: str
    text: str
    timestamp: Optional[int] = None


class MessageRequest(BaseModel):
    # Support BOTH styles
    session_id: Optional[str] = None     # old
    sessionId: Optional[str] = None      # new (GUVI)

    # message can be string OR object
    message: Union[str, NestedMessage]

    # Optional GUVI fields
    conversationHistory: Optional[List[HistoryMessage]] = []
    metadata: Optional[Dict[str, Any]] = {}


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
