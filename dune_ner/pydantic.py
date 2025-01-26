from enum import Enum

from pydantic import BaseModel


class Label(str, Enum):
    LOC = "LOC"
    PERSON = "PERSON"
    GPE = "GPE"
    NORP = "NORP"
    ORG = "ORG"


class Entity(BaseModel):
    name: str
    label: Label

    class Config:
        extra = "forbid"


class EntityList(BaseModel):
    entities: list[Entity]

    class Config:
        extra = "forbid"


class EntityChunks(BaseModel):
    chunks: dict[int, EntityList]

    class Config:
        extra = "forbid"
