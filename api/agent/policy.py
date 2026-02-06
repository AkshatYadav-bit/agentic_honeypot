from typing import Dict


class DialoguePolicy:
    """
    Decides WHAT the agent should do next.
    """

    def decide(self, session) -> Dict:
        """
        Returns a decision dict:
        {
            goal: str,
            strategy: str,
            next_action: str
        }
        """

        # 1. Before scam is confirmed
        if not session.agent_active:
            return {
                "goal": "gather_context",
                "strategy": "confused_user",
                "next_action": "ask_for_explanation"
            }

        # 2. Scam detected, engagement phase
        if session.dialogue_phase == "engagement":
            return self._engagement_policy(session)

        # 3. Payment induction phase
        if session.dialogue_phase == "payment_induction":
            return self._payment_policy(session)

        # 4. Confirmation / repetition phase
        if session.dialogue_phase == "confirmation":
            return {
                "goal": "confirm_details",
                "strategy": "anxious_user",
                "next_action":  "ask_to_confirm_details"
            }

        # Fallback
        return {
            "goal": "maintain_engagement",
            "strategy": "stall",
            "next_action": "ask_generic_question"
        }

    def _engagement_policy(self, session) -> Dict:
        """
        Build trust, induce explanation.
        """
        # Increase trust gradually
        session.trust_level += 0.1

        if session.trust_level < 0.5:
            return {
                "goal": "build_trust",
                "strategy": "fearful_but_cooperative",
                "next_action": "express_fear_and_ask_help"
            }

        # Transition to payment induction
        session.dialogue_phase = "payment_induction"
        return {
            "goal": "extract_payment_path",
            "strategy": "compliant_but_confused",
            "next_action": "ask_where_to_pay"
        }

    def _payment_policy(self, session) -> Dict:
        """
        Force scammer to reveal payment identifiers.
        """
        # Increase pressure carefully
        session.risk_level += 0.1

        if session.risk_level < 0.6:
            return {
                "goal": "extract_payment_identifier",
                "strategy": "slow_compliance",
                "next_action": "ask_for_exact_payment_details"
            }

        # Move to confirmation to avoid suspicion
        session.dialogue_phase = "confirmation"
        return {
            "goal": "verify_payment_details",
            "strategy": "double_checking_user",
            "next_action": "ask_to_confirm_details"
        }
