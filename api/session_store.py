import time
from typing import Dict, List


class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.start_time = time.time()
        self.last_updated = time.time()
        
        self.used_replies = set()
        self.final_callback_sent = False

        # Conversation memory
        self.messages: List[Dict] = []

        # Detection & agent control
        self.scam_confidence: float = 0.0
        self.agent_active: bool = False

        # Dialogue control
        self.dialogue_phase: str = "pre_detection"
        self.trust_level: float = 0.0
        self.risk_level: float = 0.0

        # Intelligence storage
        self.extracted_intelligence = {
            "upi_ids": [],
            "bank_accounts": [],
            "phishing_urls": []
        }

        # Metrics
        self.turn_count: int = 0

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        self.turn_count += 1
        self.last_updated = time.time()
        
class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id)
        return self._sessions[session_id]

    def get(self, session_id: str):
        return self._sessions.get(session_id)
