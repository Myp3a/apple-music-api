from pydantic import BaseModel, Field

from applemusic.models.meta import (
    Artwork,
    AudioVariants,
    ContentRating,
    Notes,
    PlayParameters,
)
from applemusic.models.object import AppleMusicObject


class SongPreview(BaseModel):
    """Song preview URL."""

    url: str


class SongAttributes(BaseModel):
    """Class that represents data about song.

    Attributes
    ----------
    album_name: `str`
        Album name.
    artist_name: `str`
        Artist name.
    artist_url: `str`
        Album artist URL. Can be empty.
    artwork: `Artwork`
        Data about album artwork. Can be empty.
    attribution: `str`
        Classical only. Attributed composer name.
    audio_locale: `str`
        Language of the song.
    audio_traits: List[`AudioVariants`]
        Available album audio qualities. Can be undefined.
    composer_name: `str`
        Composer name.
    content_rating: `ContentRating`
        Content rating for album. Can be unrated.
    disc_number: `int`
        Disc number. Can be empty.
    duration_in_millis: `int`
        Duration in milliseconds.
    editorial_notes: `Notes`
        Editorial notes about album. Can be empty.
    genre_names: List[`str`]
        List of song genres.
    has_credits: `bool`
        If song has credits.
    has_lyrics: `bool`
        If song has lyrics.
    has_time_synced_lyrics: `bool`
        If song has timed lyrics.
    is_apple_digital_master: `bool`
        If song was encoded with Apple Digital Master.
    is_vocal_attenuation_allowed: `bool`
        If vocal removing is possible.
    isrc: `str`
        ISRC song code.
    movement_count: `int`
        Classical only. Movement count of the song.
    movement_name: `str`
        Classical only. Movement name of the song.
    movement_number: `int`
        Classical only. Movement number of the song.
    name: `str`
        Name of album.
    play_params: `PlayParameters`
        Parameters associated with playback.
    previews: List[`SongPreview`]
        List of song preview fragments.
    release_date: `str`
        Song release date in format YYYY-MM-DD. Can be in the future for pre-releases.
        Can be undefined.
    track_number: `int`
        Album track number.
    url: `str`
        Album URL.
    work_name: `str`
        Classical only. Name of the associated work.
    """

    album_name: str = Field(alias="albumName")
    artist_name: str = Field(alias="artistName")
    artist_url: str = Field(alias="artistUrl", default="")
    artwork: Artwork = Artwork(**{})
    attribution: str = ""
    audio_locale: str = Field(alias="audioLocale", default="")
    audio_traits: list[AudioVariants] = Field(
        alias="audioTraits", default=[AudioVariants.LossyStereo]
    )
    composer_name: str = Field(alias="composerName", default="")
    content_rating: ContentRating = Field(
        alias="contentRating", default=ContentRating.No
    )
    disc_number: int = Field(alias="discNumber", default=0)
    duration_in_millis: int = Field(alias="durationInMillis")
    editorial_notes: Notes = Field(alias="editorialNotes", default=Notes(**{}))
    genre_names: list[str] = Field(alias="genreNames")
    has_credits: bool = Field(alias="hasCredits", default=False)
    has_lyrics: bool = Field(alias="hasLyrics")
    has_time_synced_lyrics: bool = Field(
        alias="hasTimeSyncedLyrics", default=False
    )
    is_apple_digital_master: bool = Field(alias="isAppleDigitalMaster")
    is_vocal_attenuation_allowed: bool = Field(
        alias="isVocalAttenuationAllowed", default=False
    )
    isrc: str = Field(alias="isrc", default="")
    movement_count: int = Field(alias="movementCount", default=0)
    movement_name: str = Field(alias="movementName", default="")
    movement_number: int = Field(alias="movementNumber", default=0)
    name: str
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    previews: list[SongPreview]
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_number: int = Field(alias="trackNumber", default=0)
    url: str
    work_name: str = Field(alias="workName", default="")


class Song(AppleMusicObject):
    """Class that represents catalog song.

    Attributes
    ----------
    id: `str`
        Unique song ID.
    type: `str`
        Object type. Should be "songs".
    href: `str`
        Song url.
    attributes: `SongAttributes`
        Song data.
    """

    attributes: SongAttributes

    def __str__(self) -> str:
        return f"Song {self.attributes.artist_name} - {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibrarySongAttributes(BaseModel):
    """Class that represents data about library song.

    Attributes
    ----------
    album_name: `str`
        Album name.
    artist_name: `str`
        Artist name.
    artwork: `Artwork`
        Data about album artwork. Can be empty.
    content_rating: `ContentRating`
        Content rating for album. Can be unrated.
    disc_number: `int`
        Disc number. Can be empty.
    duration_in_millis: `int`
        Duration in milliseconds.
    genre_names: List[`str`]
        List of song genres.
    has_lyrics: `bool`
        If song has lyrics.
    name: `str`
        Name of album.
    play_params: `PlayParameters`
        Parameters associated with playback.
    release_date: `str`
        Song release date in format YYYY-MM-DD. Can be in the future for pre-releases.
        Can be undefined.
    track_number: `int`
        Album track number.
    """

    album_name: str = Field(alias="albumName", default="")
    artist_name: str = Field(alias="artistName")
    artwork: Artwork = Artwork(**{})
    content_rating: ContentRating = Field(
        alias="contentRating", default=ContentRating.No
    )
    disc_number: int = Field(alias="discNumber", default=0)
    duration_in_millis: int = Field(alias="durationInMillis")
    genre_names: list[str] = Field(alias="genreNames")
    has_lyrics: bool = Field(alias="hasLyrics")
    name: str
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    release_date: str = Field(alias="releaseDate", default="1970-01-01")
    track_number: int = Field(alias="trackNumber", default=0)


class LibrarySong(AppleMusicObject):
    """Class that represents library song.

    Attributes
    ----------
    id: `str`
        Unique song ID.
    type: `str`
        Object type. Should be "library-songs".
    href: `str`
        Song url.
    attributes: `LibrarySongAttributes`
        Song data.
    """

    attributes: LibrarySongAttributes

    def __str__(self) -> str:
        return (
            f"LibrarySong {self.attributes.artist_name} -"
            f" {self.attributes.name}"
        )

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
