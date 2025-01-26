import re


def parse_sentence(text: str) -> list[str]:
    patterns = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|!|\?)\s+(?=[A-Z"\'])'
    sentences = re.split(patterns, text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]
