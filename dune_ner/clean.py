import json

with open("data/raw/duplicates.json", "r") as f:
    NAME_ALIASES = json.loads(f.read())


def get_entity_name(name: str) -> str:
    name = name.strip()
    for base_name, aliases in NAME_ALIASES.items():
        if name in aliases:
            return base_name
    return name
