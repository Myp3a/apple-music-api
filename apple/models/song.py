from apple.models.meta import Artwork, AudioVariants, ContentRating, PlayParameters
from apple.models.object import AppleMusicObject


class SongPreview:
    def __init__(self, data) -> None:
        self.url = data.get("url")

class SongAttributes:
    def __init__(self, data) -> None:
        self.album_name = data.get("albumName")
        self.artist_name = data.get("artistName")
        self.artist_url = data.get("artistUrl", None)
        self.artwork = Artwork(data.get("artwork", {}))
        self.attribution = data.get("attribution", "")
        self.audio_variants = [AudioVariants(el) for el in data.get("audioVariants",[None])]
        self.composer_name = data.get("composerName", "")
        self.content_rating = ContentRating(data.get("contentRating", "no"))
        self.disc_number = data.get("discNumber",0)
        self.duration_in_millis = data.get("durationInMillis")
        self.editorial_notes = data.get("editorialNotes", "")
        self.genre_names = data.get("genreNames")
        self.has_lyrics = data.get("hasLyrics")
        self.is_apple_digital_master = data.get("isAppleDigitalMaster")
        self.isrc = data.get("isrc", "")
        self.movement_count = data.get("movementCount", "")
        self.movement_name = data.get("movementName", "")
        self.movement_number = data.get("movementNumber", "")
        self.name = data.get("name")
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.previews = [SongPreview(el) for el in data.get("previews")]
        self.release_date = data.get("releaseDate","1970-01-01")
        self.track_number = data.get("trackNumber",0)
        self.url = data.get("url")
        self.work_name = data.get("workName", "")

class Song(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = SongAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"Song {self.attributes.artistName} - {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibrarySongAttributes:
    def __init__(self, data) -> None:
        self.album_name = data.get("albumName", "")
        self.artist_name = data.get("artistName")
        self.artwork = Artwork(data.get("artwork", {}))
        self.content_rating = ContentRating(data.get("contentRating", "no"))
        self.disc_number = data.get("discNumber",0)
        self.duration_in_millis = data.get("durationInMillis")
        self.genre_names = data.get("genreNames")
        self.has_lyrics = data.get("hasLyrics")
        self.name = data.get("name")
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.release_date = data.get("releaseDate","1970-01-01")
        self.track_number = data.get("trackNumber",0)

class LibrarySong(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = LibrarySongAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"LibrarySong {self.attributes.artistName} - {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
