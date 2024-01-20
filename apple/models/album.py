from apple.models.meta import Artwork, AudioVariants, ContentRating, PlayParameters
from apple.models.object import AppleMusicObject


class AlbumAttributes:
    def __init__(self, data) -> None:
        self.artist_name = data.get("artistName")
        self.artist_url = data.get("artistUrl", None)
        self.artwork = Artwork(data.get("artwork", {}))
        self.audio_variants = [AudioVariants(el) for el in data.get("audioVariants",[None])]
        self.content_rating = ContentRating(data.get("contentRating", "no"))
        self.copyright = data.get("copyright", "")
        self.editorial_notes = data.get("editorialNotes", "")
        self.genre_names = data.get("genreNames")
        self.is_compilation = data.get("isCompilation")
        self.is_complete = data.get("isComplete")
        self.is_mastered_for_itunes = data.get("isMasteredForItunes")
        self.is_single = data.get("isSingle")
        self.name = data.get("name")
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.record_label = data.get("recordLabel","")
        self.release_date = data.get("releaseDate","1970-01-01")
        self.track_count = data.get("trackCount")
        self.upc = data.get("upc","")
        self.url = data.get("url")

class Album(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = AlbumAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artistName}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibraryAlbumAttributes:
    def __init__(self, data) -> None:
        self.artist_name = data.get("artistName")
        self.artwork = Artwork(data.get("artwork", {}))
        self.content_rating = ContentRating(data.get("contentRating", "no"))
        self.date_added = data.get("dateAdded","1970-01-01")
        self.genre_names = data.get("genreNames")
        self.name = data.get("name")
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.release_date = data.get("releaseDate","1970-01-01")
        self.track_count = data.get("trackCount")

class LibraryAlbum(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = LibraryAlbumAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artistName}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
