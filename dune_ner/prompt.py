import outlines


@outlines.prompt
def extract_entities_prompt(chunk):
    """
    You are a world-class AI system trained to extract entities and part-of-speech tags from text.
    Given a text, you need to extract the entities and their corresponding tags.
    The tags can be one of the following:
    - PERSON (people, including fictional)
    - NORP (nationalities or religious or political groups)
    - ORG (organization, company, government, etc.)
    - GPE (geo-political entity, countries, cities, states)
    - LOC (non-GPE locations, mountain ranges, bodies of water)

    FORMAT: JSON, e.g. {"entities": [{"name": "John", "tag": "PERSON"}]}
    TEXT: {{ chunk }}
    RESULT:
    """
