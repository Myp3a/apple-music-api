from pydantic import BaseModel, Field

from apple.models.meta import Artwork, AudioVariants, ContentRating, Notes, PlayParameters
from apple.models.object import AppleMusicObject


class SongPreview(BaseModel):
    url: str

class SongAttributes(BaseModel):
    album_name: str = Field(alias="albumName")
    artist_name: str = Field(alias="artistName")
    artist_url: str = Field(alias="artistUrl", default="")
    artwork: Artwork = Artwork(**{})
    attribution: str = ""
    audio_variants: list[AudioVariants] = [AudioVariants.LossyStereo]
    composer_name: str = Field(alias="composerName", default="")
    content_rating: ContentRating = Field(alias="contentRating", default=ContentRating.No)
    disc_number: int = Field(alias="discNumber", default=0)
    duration_in_millis: int = Field(alias="durationInMillis")
    editorial_notes: Notes = Field(alias="editorialNotes", default=Notes(**{}))
    genre_names: list[str] = Field(alias="genreNames")
    has_lyrics: bool = Field(alias="hasLyrics")
    is_apple_digital_master: bool = Field(alias="isAppleDigitalMaster")
    isrc: str = Field(alias="isrc", default="")
    movement_count: int = Field(alias="movementCount", default=0)
    movement_name: str = Field(alias="movementName", default="")
    movement_number: int = Field(alias="movementNumber", default=0)
    name: str
    play_params: PlayParameters = Field(alias="playParams", default=PlayParameters(**{}))
    previews: list[SongPreview]
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_number: int = Field(alias="trackNumber", default=0)
    url: str
    work_name: str = Field(alias="workName", default="")

class Song(AppleMusicObject):
    attributes: SongAttributes

    def __str__(self) -> str:
        return f"Song {self.attributes.artist_name} - {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibrarySongAttributes(BaseModel):
    album_name: str = Field(alias="albumName", default="")
    artist_name: str = Field(alias="artistName")
    artwork: Artwork = Artwork(**{})
    content_rating: ContentRating = Field(alias="contentRating", default=ContentRating.No)
    disc_number: int = Field(alias="discNumber", default=0)
    duration_in_millis: int = Field(alias="durationInMillis")
    genre_names: list[str] = Field(alias="genreNames")
    has_lyrics: bool = Field(alias="hasLyrics")
    name: str
    play_params: PlayParameters = Field(alias="playParams", default=PlayParameters(**{}))
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_number: int = Field(alias="trackNumber", default=0)

class LibrarySong(AppleMusicObject):
    attributes: LibrarySongAttributes

    def __str__(self) -> str:
        return f"LibrarySong {self.attributes.artist_name} - {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
