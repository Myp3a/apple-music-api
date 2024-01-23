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
    """Class that represents data about music album.

    Attributes
    ----------
    artist_name: `str`
        Album artist name.
    artist_url: `str`
        Album artist URL. Can be empty.
    artwork: `Artwork`
        Data about album artwork. Can be empty.
    audio_traits: List[`AudioVariants`]
        Available album audio qualities. Can be undefined.
    content_rating: `ContentRating`
        Content rating for album. Can be unrated.
    copyright: `str`
        Copyright label. Can be empty.
    editorial_notes: `Notes`
        Editorial notes about album. Can be empty.
    genre_names: List[`str`]
        List of album genres.
    is_compilation: `bool`
        If album is a compilation.
    is_complete: `bool`
        If album has all tracks from it.
    is_mastered_for_itunes: `bool`
        If album was encoded with Apple Digital Master.
    is_single: `bool`
        If album is single.
    name: `str`
        Name of album.
    play_params: `PlayParameters`
        Parameters associated with playback.
    record_label: `str`
        Record label. Can be empty.
    release_date: `str`
        Album release date in format YYYY-MM-DD. Can be in the future for pre-releases.
        Can be undefined.
    track_count: `int`
        Album track count.
    upc: `str`
        UPC album code. Can be empty.
    url: `str`
        Album URL.
    """

    artist_name: str = Field(alias="artistName")
    artist_url: str = Field(alias="artistUrl", default="")
    artwork: Artwork = Artwork(**{})
    audio_traits: list[AudioVariants] = Field(
        alias="audioTraits", default=[AudioVariants.LossyStereo]
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
    is_prerelease: bool = Field(alias="isPrerelease", default=False)
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
    """Class that represents music album.

    Attributes
    ----------
    id: `str`
        Unique album ID.
    type: `str`
        Object type. Should be "albums".
    href: `str`
        Album url.
    attributes: `AlbumAttributes`
        Album data.
    """

    attributes: AlbumAttributes

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artist_name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryAlbumAttributes(BaseModel):
    """Class that represents data about music album.

    Attributes
    ----------
    artist_name: `str`
        Album artist name.
    artwork: `Artwork`
        Data about album artwork. Can be empty.
    content_rating: `ContentRating`
        Content rating for album. Can be unrated.
    date_added: `str`
        Album addition date in format YYYY-MM-DD.
    genre_names: List[`str`]
        List of album genres.
    name: `str`
        Name of album.
    play_params: `PlayParameters`
        Parameters associated with playback.
    release_date: `str`
        Album release date in format YYYY-MM-DD. Can be in the future for pre-releases.
        Can be undefined.
    track_count: `int`
        Album track count.
    """

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
    """Class that represents library music album.

    Attributes
    ----------
    id: `str`
        Unique album ID.
    type: `str`
        Object type. Should be "library-albums".
    href: `str`
        Album url.
    attributes: `LibraryAlbumAttributes`
        Album data.
    """

    attributes: LibraryAlbumAttributes

    def __str__(self) -> str:
        return f"Album {self.attributes.name} - {self.attributes.artist_name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
