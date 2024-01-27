from typing import List

from pydantic import BaseModel


class Relationship(BaseModel):
    """Specific relationship between source and other object.

    Attributes
    ----------
    id: `str`
        ID of related object.
    type: `str`
        Type of related object.
    href: `str`
        URL of related object.
    """

    id: str
    type: str
    href: str


class RelationshipArray(BaseModel):
    """Generic class for relationships.

    Attributes
    ----------
    href: `str`
        URL of relationships endpoint
    data: List[`Relationship`]
        Actual relationships.
    """

    href: str = ""
    data: List[Relationship] = []


class Relationships(BaseModel):
    """Container of various relationships.

    Attributes
    ----------
    albums: `RelationshipArray`
        Albums relationships.
    artists: `RelationshipArray`
        Artists relationships.
    """

    albums: RelationshipArray = RelationshipArray(**{})
    artists: RelationshipArray = RelationshipArray(**{})
