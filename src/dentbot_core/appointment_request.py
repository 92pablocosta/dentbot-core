class AppointmentRequest:
    def __init__(self, patient_name: str, care_type: str):

        if not patient_name.strip():
            raise ValueError("patient_name cannot be empty")
        
        if not care_type.strip():
            raise ValueError("care_type cannot be empty")

        self.patient_name = patient_name.strip()
        self.care_type = care_type.strip()
        self.status = "pending"
    