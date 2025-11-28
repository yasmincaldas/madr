import re


def sanitize_string(data: str) -> str:
    data = data.casefold().strip()
    data = re.sub(r'[^a-zà-ú\s]', '', data)
    data = ' '.join(data.split())
    return data