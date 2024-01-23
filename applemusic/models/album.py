from pydantic import BaseModel, Field

from applemusic.models.meta import (
    Artwork,
    AudioVariants,
    ContentRating,
    Notes,
    PlayParameters,
)
from applemusic.models.object import AppleMusicObject


class AlbumAttributes(BaseModel):
    artist_name: str = Field(alias="artistName")
    artist_url: str = Field(alias="artistUrl", default="")
    artwork: Artwork = Artwork(**{})
    audio_variants: list[AudioVariants] = Field(
        alias="audioVariants", default=[AudioVariants.Undefined]
    )
    content_rating: ContentRating = Field(
        alias="contentRating", default=ContentRating.No
    )
    copyright: str = ""
    editorial_notes: Notes = Field(alias="editorialNotes", default=Notes(**{}))
    genre_names: list[str] = Field(alias="genreNames")
    is_compilation: bool = Field(alias="isCompilation")
    is_complete: bool = Field(alias="isComplete")
    is_mastered_for_itunes: bool = Field(alias="isMasteredForItunes")
    is_single: bool = Field(alias="isSingle")
    name: str
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    record_label: str = Field(alias="recordLabel", default="")
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_count: int = Field(alias="trackCount")
    upc: str = ""
    url: str


class Album(AppleMusicObject):
    attributes: AlbumAttributes

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artist_name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryAlbumAttributes(BaseModel):
    artist_name: str = Field(alias="artistName")
    artwork: Artwork = Artwork(**{})
    content_rating: ContentRating = Field(
        alias="contentRating", default=ContentRating.No
    )
    date_added: str = Field(alias="dateAdded", default="1970-01-01")
    genre_names: list[str] = Field(alias="genreNames")
    name: str
    play_params: PlayParameters = PlayParameters(**{})
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_count: int = Field(alias="trackCount")


class LibraryAlbum(AppleMusicObject):
    attributes: LibraryAlbumAttributes

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artist_name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
