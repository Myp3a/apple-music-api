from pydantic import BaseModel, Field

from applemusic.models.meta import Artwork, Notes
from applemusic.models.object import AppleMusicObject


class ArtistAttributes(BaseModel):
    """Class that represents data about music artist.
    Not meant to be used directly.
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
    artwork: `Artwork`
        Data about artist artwork. Can be empty.
    editorial_notes: `Notes`
        Editorial notes about artist. Can be empty.
    genre_names: list[`str`]
        List of artist genres.
    name: `str`
        Artist name.
    url: `str`
        Artist URL.
    """

    attributes: ArtistAttributes

    @property
    def artwork(self) -> Artwork:
        return self.attributes.artwork

    @property
    def editorial_notes(self) -> Notes:
        return self.attributes.editorial_notes

    @property
    def genre_names(self) -> list[str]:
        return self.attributes.artwork

    @property
    def name(self) -> str:
        return self.attributes.name

    @property
    def url(self) -> str:
        return self.attributes.url

    def __str__(self) -> str:
        return f"Artist {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryArtistAttributes(BaseModel):
    """Class that represents data about library music artist.
    Not meant to be used directly.
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
    name: `str`
        Artist name.
    """

    attributes: LibraryArtistAttributes

    @property
    def name(self) -> str:
        return self.attributes.name

    def __str__(self) -> str:
        return f"LibraryArtist {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
