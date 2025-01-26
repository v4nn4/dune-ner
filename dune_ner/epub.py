import re

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()


def clean_text(text: str) -> str:
    text = text.replace("\u2019", "'")  # Replace right single quotes
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # Replace double quotes
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text.strip()


def extract_chapter(file_path: str, chapter_id: int) -> str:
    book = epub.read_epub(file_path, options={"ignore_ncx": False})
    chapters = [
        item.get_content().decode("utf-8")
        for item in book.get_items()
        if item.get_type() == ebooklib.ITEM_DOCUMENT
    ]
    first_chapter = chapters[chapter_id]
    cleaned_text = clean_text(clean_html(first_chapter))
    return cleaned_text
