def sanitize_string(cls, value: str) -> str:
    value = value.strip()
    value = value.lower()
    value = re.sub(r'\s+', ' ', value)
    return value