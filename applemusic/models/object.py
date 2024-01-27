from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from applemusic.models.relationships import Relationships

if TYPE_CHECKING:
    from applemusic.client import ApiClient


class AppleMusicObject(BaseModel):
    """Class that represents basic Apple Music object.

    Attributes
    ----------
    id: `str`
        Unique ID.
    type: `str`
        Object type.
    href: `str`
        URL.
    attributes: `ArtistAttributes`
        Specific data.
    relationships: `Relationships`
        Relationships to other objects.
    views: `dict`
        ?
    """

    id: str
    type: str
    href: str = ""
    attributes: str
    relationships: Relationships = Relationships(**{})
    views: dict = {}
    _client: ApiClient

    def __init__(self, client, **data):
        super().__init__(**data)
        self._client = client
