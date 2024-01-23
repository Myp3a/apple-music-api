from pydantic import BaseModel, Field

from applemusic.models.meta import Artwork, Notes
from applemusic.models.object import AppleMusicObject


class ArtistAttributes(BaseModel):
    """Class that represents data about music artist.

    Attributes
    ----------
    artwork: `Artwork`
        Data about artist artwork. Can be empty.
    editorial_notes: `Notes`
        Editorial notes about artist. Can be empty.
    genre_names: List[`str`]
        List of artist genres.
    name: `str`
        Artist name.
    url: `str`
        Artist URL.
    """

    artwork: Artwork = Artwork(**{})
    editorial_notes: Notes = Field(alias="editorialNotes", default=Notes(**{}))
    genre_names: list[str] = Field(alias="genreNames")
    name: str
    url: str


class Artist(AppleMusicObject):
    """Class that represents music artist.

    Attributes
    ----------
    id: `str`
        Unique artist ID.
    type: `str`
        Object type. Should be "artists".
    href: `str`
        Artist url.
    attributes: `ArtistAttributes`
        Artist data.
    """

    attributes: ArtistAttributes

    def __str__(self) -> str:
        return f"Artist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryArtistAttributes(BaseModel):
    """Class that represents data about library music artist.

    Attributes
    ----------
    name: `str`
        Artist name.
    """

    name: str


class LibraryArtist(AppleMusicObject):
    """Class that represents library music artist.

    Attributes
    ----------
    id: `str`
        Unique artist ID.
    type: `str`
        Object type. Should be "library-artists".
    href: `str`
        Artist url.
    attributes: `LibraryArtistAttributes`
        Artist data.
    """

    attributes: LibraryArtistAttributes

    def __str__(self) -> str:
        return f"LibraryArtist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
