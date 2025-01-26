import outlines
from tqdm import tqdm

from dune_ner.data import read_chapter, write_entity_chunks
from dune_ner.parse import parse_sentence
from dune_ner.prompt import extract_entities_prompt
from dune_ner.pydantic import EntityChunks, EntityList


def create_entities_outlines(
    model: str = "gpt-4o-mini",
    window_size: int = 10,
    overlap: int = 2,
):
    all_chunks = []
    for i in tqdm(range(1, 8)):
        chapter_text = read_chapter(i)
        sentences = parse_sentence(chapter_text)
        chunks = [
            ". ".join(sentences[i : i + window_size])
            for i in range(0, len(sentences) - overlap, window_size - overlap)
        ]
        all_chunks.extend(chunks)
    all_prompts = [extract_entities_prompt(chunk) for chunk in all_chunks]
    model = outlines.models.openai(model)
    generator = outlines.generate.json(model, EntityList)
    results = {}
    for i, prompt in tqdm(enumerate(all_prompts), total=len(all_prompts)):
        generated_result = generator(prompt)
        results[i] = generated_result
    entity_chunks = EntityChunks(chunks=results)
    write_entity_chunks(entity_chunks)
