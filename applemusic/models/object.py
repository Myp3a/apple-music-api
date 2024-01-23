from pydantic import BaseModel


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
    relationships: `dict`
        Relationships to other objects.
    views: `dict`
        ?
    """

    id: str
    type: str
    href: str = ""
    attributes: str
    relationships: dict = {}
    views: dict = {}
