from pydantic import BaseModel, Field

from apple.models.meta import Artwork, Notes
from apple.models.object import AppleMusicObject


class ArtistAttributes(BaseModel):
    artwork: Artwork = Artwork(**{})
    editorial_notes: Notes = Field(alias="editorialNotes", default=Notes(**{}))
    genre_names: list[str] = Field(alias="genreNames")
    name: str
    url: str

class Artist(AppleMusicObject):
    attributes: ArtistAttributes

    def __str__(self) -> str:
        return f"Artist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibraryArtistAttributes(BaseModel):
    name: str

class LibraryArtist(AppleMusicObject):
    attributes: LibraryArtistAttributes

    def __str__(self) -> str:
        return f"LibraryArtist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
