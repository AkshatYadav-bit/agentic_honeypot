import random


TEMPLATES = {
    "ask_for_explanation": [
        "Sorry, I don’t really understand. What is this about?",
        "I’m confused… why is this happening to me?",
        "Can you please explain what I did wrong?"
    ],

    "express_fear_and_ask_help": [
        "I’m really scared right now… will my account be okay?",
        "Please help me, I don’t want any problem.",
        "I’m worried, I’ve never faced this before."
    ],

    "ask_where_to_pay": [
        "Okay… what do I need to do now?",
        "Where exactly should I make the payment?",
        "Can you tell me how to fix this?"
    ],

    "ask_for_exact_payment_details": [
        "I don’t want to make a mistake. Where exactly should I send it?",
        "Please tell me the exact details so I do it correctly.",
        "Which account or UPI should I use?"
    ],

    "ask_to_confirm_details": [
        "Just to be sure, can you send the details again?",
        "I want to double-check before doing anything.",
        "Please confirm the payment information once more."
    ],

    "ask_generic_question": [
        "Okay… what should I do next?",
        "Can you guide me?",
        "Please explain again."
    ]
}


class Responder:
    def generate(self, action: str) -> str:
        options = TEMPLATES.get(action)
        if not options:
            return "I’m not sure what to do. Can you help?"

        return random.choice(options)
