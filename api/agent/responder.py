import random


TEMPLATES = {
    "ask_for_explanation": [
    "Sorry, I don’t really understand. What is this about?",
    "I’m confused… why is this happening to me?",
    "Can you please explain what I did wrong?",
    "I don’t recall doing anything unusual. What’s the issue?",
    "This is the first time I’m hearing about this. Can you explain?",
    "I’m not very tech-savvy, could you tell me what this means?",
    "Why would my account have a problem suddenly?",
    "Can you explain this in simple words? I’m not sure I follow."
    ],

    "express_fear_and_ask_help": [
    "I’m really scared right now… will my account be okay?",
    "Please help me, I don’t want any problem.",
    "I’m worried, I’ve never faced this before.",
    "This is making me anxious, I don’t know what to do.",
    "I’m afraid something bad might happen to my money.",
    "I’m really stressed after reading this message.",
    "I don’t understand these things and it’s making me panic.",
    "Please guide me, I’m very nervous about this."        
    ],

    "ask_where_to_pay": [
    "Okay… what do I need to do now?",
    "Where exactly should I make the payment?",
    "Can you tell me how to fix this?",
    "What steps should I follow to resolve this issue?",
    "How can I complete the verification?",
    "What should I do so my account is not blocked?",
    "Can you guide me step by step?",
    "What is the process to make this right?"
    ],

    "ask_for_exact_payment_details": [
    "I don’t want to make a mistake. Where exactly should I send it?",
    "Please tell me the exact details so I do it correctly.",
    "Which account or UPI should I use?",
    "Can you share the exact payment details?",
    "I want to be careful, can you give me the full information?",
    "Please send the payment details clearly.",
    "Where should I transfer the amount?",
    "Can you confirm the correct account details for payment?"
    ],

    "ask_to_confirm_details": [
    "Just to be sure, can you send the details again?",
    "I want to double-check before doing anything.",
    "Please confirm the payment information once more.",
    "Can you repeat the details so I don’t get it wrong?",
    "I’m worried about making a mistake, can you confirm again?",
    "Before I proceed, can you verify the details?",
    "I want to be absolutely sure — can you resend the information?",
    "Please confirm everything one last time."
    ],

    "ask_generic_question": [
    "Okay… what should I do next?",
    "Can you guide me?",
    "Please explain again.",
    "What happens after this?",
    "Can you clarify this for me?",
    "What is the next step from my side?",
    "I’m still unsure, what should I do?",
    "Can you help me understand what comes next?"
    ]
}


class Responder:
    def generate(self, action: str, session) -> str:
        options = TEMPLATES.get(action)

        if not options:
            return "I’m not sure what to do. Can you help?"

        # Initialize per-action counter
        if action not in session.action_counters:
            session.action_counters[action] = 0

        index = session.action_counters[action] % len(options)
        reply = options[index]

        session.action_counters[action] += 1
        return reply

