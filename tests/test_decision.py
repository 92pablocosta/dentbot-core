from dentbot_core.decision import Decision, make_decision


def test_decision_stores_structured_data():
    decision = Decision(
        intent="pricing_question",
        action="pricing_response",
        message="A consulta custa R$ 250",
    )
    assert decision.intent == "pricing_question"
    assert decision.action == "pricing_response"
    assert decision.message == "A consulta custa R$ 250"


def test_makes_pricing_decision():
    result = make_decision("Qual é o valor da consulta?")

    assert result == Decision(
        intent="pricing_question",
        action="pricing_response",
        message="A consulta custa R$ 250. Os demais serviços são avaliados durante a consulta.",
    )


def test_makes_appointment_decision():
    result = make_decision("Quero marcar uma consulta")

    assert result == Decision(
        intent="appointment_request",
        action="appointment_intake",
        message="Para iniciar o agendamento, preciso de algumas informações.",
    )


def test_makes_emergency_decision():
    result = make_decision("Estou com um sangramento")

    assert result == Decision(
        intent="emergency",
        action="emergency_triage",
        message="Para avaliar a urgência, preciso do seu nome completo e de uma descrição dos sintomas.",
    )


def test_makes_human_handoff_decision():
    result = make_decision("Oi, tudo bem?")

    assert result == Decision(
        intent="other",
        action="human_handoff",
        message="Vou encaminhar sua mensagem para o atendimento humano.",
    )