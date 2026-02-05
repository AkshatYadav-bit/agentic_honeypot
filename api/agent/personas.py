import random


class Persona:
    def __init__(self, name, style, fear_level):
        self.name = name
        self.style = style
        self.fear_level = fear_level


# Define personas
PERSONAS = {
    "elderly_confused": Persona(
        name="elderly_confused",
        style="slow, polite, confused",
        fear_level=0.7
    ),
    "busy_worker": Persona(
        name="busy_worker",
        style="short, impatient, distracted",
        fear_level=0.4
    ),
    "naive_student": Persona(
        name="naive_student",
        style="respectful, anxious, unsure",
        fear_level=0.6
    )
}


def select_persona(session):
    """
    Choose persona based on risk & trust.
    """
    if session.trust_level < 0.4:
        return PERSONAS["elderly_confused"]

    if session.risk_level > 0.5:
        return PERSONAS["busy_worker"]

    return PERSONAS["naive_student"]
