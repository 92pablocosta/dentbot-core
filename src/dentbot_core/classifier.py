def classify_intent(message: str) -> str:
    text = message.strip().lower()
    
    appointment_keywords = ["marcar", "consulta", "horário", "disponível"]
    emergency_keywords = ["urgente", "emergência", "sangramento", "inchaço"]
    pricing_keywords = ["preço", "valor", "quanto custa"]

    for word in emergency_keywords:
        if word in text:
            return "emergency"

    for word in pricing_keywords:
        if word in text:
            return "pricing_question"

    for word in appointment_keywords:
        if word in text:
            return "appointment_request"
    
    return "other"

