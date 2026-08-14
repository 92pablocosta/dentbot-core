from dentbot_core.classifier import classify_intent


def test_classifies_appointment_request():
    result = classify_intent("Quero marcar uma consulta")

    assert result == "appointment_request"

def test_classifies_emergency_request():
    result = classify_intent("Estou com um SANGRAMENTO")

    assert result == "emergency"

def test_classifies_pricing_request():
    result = classify_intent("Qual é o valor da consulta?")

    assert result == "pricing_question"

def test_other_request():
    result = classify_intent("oi, td bem?")

    assert result == "other"


def test_emergency_has_priority_over_appointment():
    result = classify_intent("Quero marcar uma consulta urgente")

    assert result == "emergency"