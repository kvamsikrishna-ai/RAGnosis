import re

def clean_text(text: str) -> str:
    # remove headers/footers artifacts
    text = re.sub(r'Page \d+ of \d+', '', text)

    # normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # remove weird characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    return text.strip()