from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Formats datetime object to a readable string."""
    if dt is not None:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

def calculate_delivery_time(registered_time: datetime, delivery_hours: int) -> datetime:
    """Calculates the expected delivery time based on registered time and delivery hours."""
    return registered_time + timedelta(hours=delivery_hours)

def email_validator(email: str) -> bool:
    """Validates the format of an email address."""
    import re
    pattern = r"^\S+@\S+\.\S+$"
    return re.match(pattern, email) is not None
