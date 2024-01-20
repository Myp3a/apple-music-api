from apple.models.meta import Artwork
from apple.models.object import AppleMusicObject


class ArtistAttributes:
    def __init__(self, data) -> None:
        self.artwork = Artwork(data.get("artwork", {}))
        self.editorial_notes = data.get("editorialNotes", "")
        self.genre_names = data.get("genreNames")
        self.name = data.get("name")
        self.url = data.get("url")

class Artist(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = ArtistAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"Artist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibraryArtistAttributes:
    def __init__(self, data) -> None:
        self.name = data.get("name")

class LibraryArtist(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = LibraryArtistAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"LibraryArtist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
