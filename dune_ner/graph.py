import networkx as nx

from dune_ner.clean import get_entity_name
from dune_ner.data import export_graph, read_entity_chunks


def export_entity_graph():
    entities_chunks = read_entity_chunks()
    graph = nx.Graph()
    for _, entities_obj in entities_chunks.chunks.items():
        entity_names = [
            get_entity_name(entity.name)
            for entity in entities_obj.entities
            if entity.label == "PERSON"
        ]
        for i in range(len(entity_names)):
            for j in range(i + 1, len(entity_names)):
                entity1, entity2 = entity_names[i], entity_names[j]
                if graph.has_edge(entity1, entity2):
                    graph[entity1][entity2]["weight"] += 1
                else:
                    graph.add_edge(entity1, entity2, weight=1)
    graph = nx.Graph(
        (u, v, e) for u, v, e in graph.edges(data=True) if e["weight"] > 10
    )
    export_graph(graph)
