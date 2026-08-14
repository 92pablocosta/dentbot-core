from dataclasses import dataclass

from dentbot_core.classifier import classify_intent


@dataclass
class Decision:
    intent: str
    action: str
    message: str


def make_decision(message: str) -> Decision:
    intent = classify_intent(message)

    if intent == "pricing_question":
        return Decision(
            intent="pricing_question",
            action="pricing_response",
            message="A consulta custa R$ 250. Os demais serviços são avaliados durante a consulta.",
        )

    if intent == "appointment_request":
        return Decision(
            intent="appointment_request",
            action="appointment_intake",
            message="Para iniciar o agendamento, preciso de algumas informações.",
        )

    if intent == "emergency":
        return Decision(
            intent="emergency",
            action="emergency_triage",
            message="Para avaliar a urgência, preciso do seu nome completo e de uma descrição dos sintomas.",
        )

    if intent == "other":
        return Decision(
            intent="other",
            action="human_handoff",
            message="Vou encaminhar sua mensagem para o atendimento humano.",
        )

    raise NotImplementedError(
        f"Decision mapping is not implemented for intent: {intent}"
    )
