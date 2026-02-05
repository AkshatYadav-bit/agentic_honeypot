import time


class MetricsEngine:
    def update(self, session):
        """
        Update and return metrics snapshot for response.
        """
        duration = int(time.time() - session.start_time)

        return {
            "conversation_turns": session.turn_count,
            "engagement_duration_sec": duration,
            "dialogue_phase": session.dialogue_phase,
            "agent_active": session.agent_active,
            "intel_count": {
                "upi_ids": len(session.extracted_intelligence["upi_ids"]),
                "bank_accounts": len(session.extracted_intelligence["bank_accounts"]),
                "phishing_urls": len(session.extracted_intelligence["phishing_urls"]),
            }
        }
