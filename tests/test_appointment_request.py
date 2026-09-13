import pytest
from dentbot_core.appointment_request import AppointmentRequest


def test_appointment_request_starts_pending():
    request = AppointmentRequest("Pablo", "limpeza")

    assert request.patient_name == "Pablo"
    assert request.care_type == "limpeza"
    assert request.status == "pending"


def test_appointment_request_rejects_empty_patient_name():
    with pytest.raises(ValueError):
        AppointmentRequest("  ", "limpeza")


def test_appointment_request_rejects_empty_care_type():
    with pytest.raises(ValueError):
        AppointmentRequest("Pablo", "   ")


def test_appointment_request_strips_input_whitespace():
    request = AppointmentRequest("  Pablo  ", "  limpeza  ")

    assert request.patient_name == "Pablo"
    assert request.care_type == "limpeza"
