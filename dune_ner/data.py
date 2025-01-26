import json
import os

import networkx as nx

from dune_ner.pydantic import EntityChunks

GENERATED_DATA_PATH = "data/generated"
CHAPTER_FILENAME = "chapter{}.txt"
ENTITY_CHUNKS_FILENAME = "entity_chunks.json"
ENTITY_GRAPH_FILENAME = "entity_graph.json"
ENTITY_EDGES_FILENAME = "entity_edges.csv"


def read_chapter(chapter_id: int) -> str:
    if not os.path.exists(
        os.path.join(GENERATED_DATA_PATH, CHAPTER_FILENAME.format(chapter_id))
    ):
        raise FileNotFoundError(f"Chapter {chapter_id} not found")
    with open(
        os.path.join(GENERATED_DATA_PATH, f"chapter{chapter_id}.txt"), "r"
    ) as file:
        return file.read()


def write_chapter(chapter_id: int, text: str):
    os.makedirs(GENERATED_DATA_PATH, exist_ok=True)
    with open(
        os.path.join(GENERATED_DATA_PATH, f"chapter{chapter_id}.txt"), "w"
    ) as file:
        file.write(text)


def write_entity_chunks(results: EntityChunks, filename: str = ENTITY_CHUNKS_FILENAME):
    os.makedirs(GENERATED_DATA_PATH, exist_ok=True)
    with open(os.path.join(GENERATED_DATA_PATH, filename), "w") as file:
        file.write(results.model_dump_json(indent=4))


def read_entity_chunks():
    if not os.path.exists(os.path.join(GENERATED_DATA_PATH, ENTITY_CHUNKS_FILENAME)):
        raise FileNotFoundError("Entity chunks not found")
    with open(os.path.join(GENERATED_DATA_PATH, ENTITY_CHUNKS_FILENAME), "r") as file:
        return EntityChunks.model_validate_json(file.read())


def export_graph(graph: nx.Graph):
    os.makedirs(GENERATED_DATA_PATH, exist_ok=True)
    graph_json = nx.readwrite.json_graph.node_link_data(graph)
    with open(os.path.join(GENERATED_DATA_PATH, ENTITY_GRAPH_FILENAME), "w") as file:
        json.dump(graph_json, file, indent=4)
    nx.write_edgelist(
        graph,
        os.path.join(GENERATED_DATA_PATH, ENTITY_EDGES_FILENAME),
        delimiter=",",
        data=["count"],
    )
