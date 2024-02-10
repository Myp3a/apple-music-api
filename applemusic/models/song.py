from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from applemusic.models.album import Album
from applemusic.models.artist import Artist
from applemusic.models.meta import (
    Artwork,
    AudioVariants,
    CatalogTypes,
    ContentRating,
    Notes,
    PlayParameters,
)
from applemusic.models.object import AppleMusicObject

if TYPE_CHECKING:
    from applemusic.models.lyrics import Lyrics


class SongPreview(BaseModel):
    """Song preview URL."""

    url: str


class SongAttributes(BaseModel):
    """Class that represents data about song.
    Not meant to be used directly.
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
    audio_traits: list[`AudioVariants`]
        Available song audio qualities. Can be undefined.
    composer_name: `str`
        Composer name.
    content_rating: `ContentRating`
        Content rating for song. Can be unrated.
    disc_number: `int`
        Disc number. Can be empty.
    duration_in_millis: `int`
        Duration in milliseconds.
    editorial_notes: `Notes`
        Editorial notes about song. Can be empty.
    genre_names: list[`str`]
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
        Name of song.
    play_params: `PlayParameters`
        Parameters associated with playback.
    previews: list[`SongPreview`]
        List of song preview fragments.
    release_date: `str`
        Song release date in format YYYY-MM-DD. Can be in the future for pre-releases.
        Can be undefined.
    track_number: `int`
        Album track number.
    url: `str`
        Song URL.
    work_name: `str`
        Classical only. Name of the associated work.
    """

    attributes: SongAttributes

    @property
    def album_name(self) -> str:
        return self.attributes.album_name

    @property
    def artist_name(self) -> str:
        return self.attributes.artist_name

    @property
    def artist_url(self) -> str:
        return self.attributes.artist_url

    @property
    def artwork(self) -> Artwork:
        return self.attributes.artwork

    @property
    def audio_locale(self) -> str:
        return self.attributes.audio_locale

    @property
    def audio_traits(self) -> list[AudioVariants]:
        return self.attributes.audio_traits

    @property
    def composer_name(self) -> str:
        return self.attributes.composer_name

    @property
    def content_rating(self) -> ContentRating:
        return self.attributes.content_rating

    @property
    def disc_number(self) -> int:
        return self.attributes.disc_number

    @property
    def duration_in_millis(self) -> int:
        return self.attributes.duration_in_millis

    @property
    def editorial_notes(self) -> Notes:
        return self.attributes.editorial_notes

    @property
    def genre_names(self) -> list[str]:
        return self.attributes.genre_names

    @property
    def has_credits(self) -> bool:
        return self.attributes.has_credits

    @property
    def has_lyrics(self) -> bool:
        return self.attributes.has_lyrics

    @property
    def has_time_synced_lyrics(self) -> bool:
        return self.attributes.has_time_synced_lyrics

    @property
    def is_apple_digital_master(self) -> bool:
        return self.attributes.is_apple_digital_master

    @property
    def is_vocal_attenuation_allowed(self) -> bool:
        return self.attributes.is_vocal_attenuation_allowed

    @property
    def isrc(self) -> str:
        return self.attributes.isrc

    @property
    def movement_count(self) -> int:
        return self.attributes.movement_count

    @property
    def movement_name(self) -> str:
        return self.attributes.movement_name

    @property
    def movement_number(self) -> int:
        return self.attributes.movement_number

    @property
    def name(self) -> str:
        return self.attributes.name

    @property
    def play_params(self) -> PlayParameters:
        return self.attributes.play_params

    @property
    def previews(self) -> list[SongPreview]:
        return self.attributes.previews

    @property
    def release_date(self) -> str:
        return self.attributes.release_date

    @property
    def track_number(self) -> int:
        return self.attributes.track_number

    @property
    def url(self) -> str:
        return self.attributes.url

    @property
    def work_name(self) -> str:
        return self.attributes.work_name

    def __str__(self) -> str:
        return f"Song {self.artist_name} - {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

    def add_to_library(self) -> bool:
        """`bool`: Adds song to user library.

        Needs Music User Token.
        """
        return self._client.library.add(self)

    def album(self) -> Album:
        """`Album`: Returns album containing the song."""
        song = self._client.catalog.get_by_id(self.id, CatalogTypes.Songs)
        assert song is not None
        album = self._client.catalog.get_by_id(
            song.relationships.albums.data[0].id, CatalogTypes.Albums
        )
        assert isinstance(album, Album)
        return album

    def artist(self) -> Album:
        """`Artist`: Returns artist performing the song."""
        song = self._client.catalog.get_by_id(self.id, CatalogTypes.Songs)
        assert song is not None
        artist = self._client.catalog.get_by_id(
            song.relationships.artists.data[0].id, CatalogTypes.Artists
        )
        assert isinstance(artist, Artist)
        return artist

    def audio(self) -> bytes:
        """`bytes`: Returns raw decrypted music data.

        Needs a Music User Token.

        Needs a Widevine device file.
        """
        return self._client.playback.get_decrypted_audio(self)

    def get_library_song(self, fast=True) -> LibrarySong | None:
        """`LibrarySong`|`None`: Returns matching song in user library.

        Needs Music User Token.

        Arguments
        ---------
        fast: `bool`
            Use faster query mechanism, but sometimes unreliable.
        """
        return self._client.library.get_corresponding_library_song(self, fast)

    def in_library(self, fast=True) -> bool:
        """`bool`: Returns if song is in user's music library.

        Needs Music User Token.

        Arguments
        ---------
        fast: `bool`
            Use faster query mechanism, but sometimes unreliable.
        """
        if self.get_library_song(fast) is not None:
            return True
        return False

    def lyrics(self) -> Lyrics | None:
        """`Lyrics`|`None`: Returns lyrics for song, `None` if not exists."""
        return self._client.catalog.lyrics(self)

    def get_artwork(self) -> bytes:
        return self._client.catalog.get_artwork(self)


class LibrarySongAttributes(BaseModel):
    """Class that represents data about library song.
    Not meant to be used directly.
    """

    album_name: str = Field(alias="albumName", default="")
    artist_name: str = Field(alias="artistName", default="")
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
    album_name: `str`
        Album name. Can be empty.
    artist_name: `str`
        Artist name. Can be empty.
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

    attributes: LibrarySongAttributes

    @property
    def album_name(self) -> str:
        return self.attributes.album_name

    @property
    def artist_name(self) -> str:
        return self.attributes.artist_name

    @property
    def artwork(self) -> Artwork:
        return self.attributes.artwork

    @property
    def content_rating(self) -> ContentRating:
        return self.attributes.content_rating

    @property
    def disc_number(self) -> int:
        return self.attributes.disc_number

    @property
    def duration_in_millis(self) -> int:
        return self.attributes.duration_in_millis

    @property
    def genre_names(self) -> list[str]:
        return self.attributes.genre_names

    @property
    def has_lyrics(self) -> bool:
        return self.attributes.has_lyrics

    @property
    def name(self) -> str:
        return self.attributes.name

    @property
    def play_params(self) -> PlayParameters:
        return self.attributes.play_params

    @property
    def release_date(self) -> str:
        return self.attributes.release_date

    @property
    def track_number(self) -> int:
        return self.attributes.track_number

    def __str__(self) -> str:
        return f"LibrarySong {self.artist_name} - {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

    def audio(self) -> bytes | None:
        """`bytes`: Returns raw decrypted music data.

        Needs a Music User Token.

        Needs a Widevine device file.
        """
        if (catalog_song := self.get_catalog_song()) is not None:
            return self._client.playback.get_decrypted_audio(catalog_song)
        return None

    def get_catalog_song(self) -> Song | None:
        """`Song`|`None`: Returns corresponding catalog song, `None` if not exists."""
        return self._client.catalog.get_corresponding_catalog_song(self)

    def lyrics(self) -> Lyrics | None:
        """`Lyrics`|`None`: Returns lyrics for song, `None` if not exists."""
        if (catalog_song := self.get_catalog_song()) is None:
            return None
        return self._client.catalog.lyrics(catalog_song)

    def remove_from_library(self) -> bool:
        """`bool`: Removes song from user library.

        Needs Music User Token.
        """
        return self._client.library.remove(self)

    def get_artwork(self) -> bytes:
        return self._client.catalog.get_artwork(self)
