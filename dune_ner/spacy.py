import spacy
from tqdm import tqdm

from dune_ner.data import read_chapter, write_entity_chunks
from dune_ner.parse import parse_sentence
from dune_ner.pydantic import Entity, EntityChunks, EntityList, Label

SPACY_MODEL = "en_core_web_lg"


def create_entities_spacy(window_size: int = 10, overlap: int = 2):
    nlp = spacy.load(SPACY_MODEL)
    all_chunks = []
    for i in tqdm(range(1, 8)):
        chapter_text = read_chapter(i)
        sentences = parse_sentence(chapter_text)
        chunks = [
            ". ".join(sentences[i : i + window_size])
            for i in range(0, len(sentences) - overlap, window_size - overlap)
        ]
        all_chunks.extend(chunks)
    available_tags = [t.name for t in Label]
    results = {}
    for i, chunk in tqdm(enumerate(all_chunks), total=len(all_chunks)):
        result = nlp(chunk)
        results[i] = EntityList(
            entities=[
                Entity(name=r.text, label=r.label_)
                for r in result.ents
                if r.label_ in available_tags
            ]
        )
    entity_chunks = EntityChunks(chunks=results)
    write_entity_chunks(entity_chunks, filename="entity_chunks_spacy.json")
