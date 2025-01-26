import os

import fire

from dune_ner.data import write_chapter
from dune_ner.epub import extract_chapter
from dune_ner.graph import export_entity_graph
from dune_ner.outlines import create_entities_outlines
from dune_ner.spacy import create_entities_spacy


class DuneApp:
    def extract_chapters(
        self,
        file_path: str = "data/raw/book.epub",
        chapter_start: int = 1,
        n_chapters: int = 7,
    ):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        for i in range(chapter_start, n_chapters - chapter_start + 2):
            text = extract_chapter(file_path, i)
            write_chapter(i, text)

    def create_entities(
        self,
        model: str = "spacy",
        window_size: int = 10,
        overlap: int = 2,
    ):
        if model == "spacy":
            create_entities_spacy(window_size, overlap)
        elif model == "outlines":
            create_entities_outlines("gpt-4o-mini", window_size, overlap)
        else:
            raise ValueError("Invalid model")

    def export_entity_graph(self):
        export_entity_graph()


if __name__ == "__main__":
    fire.Fire(DuneApp)
