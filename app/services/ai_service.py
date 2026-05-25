def generate_summary(text: str):

    if len(text) < 300:
        return text

    return text[:300]