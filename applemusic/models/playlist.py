from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from applemusic.models.meta import Artwork, Notes, PlayParameters
from applemusic.models.object import AppleMusicObject

if TYPE_CHECKING:
    from applemusic.models.song import LibrarySong, Song


class PlaylistTrackTypes(Enum):
    """Playlist tracks type."""

    Undefined = None
    MusicVideos = "music-videos"
    Songs = "songs"


class PlaylistType(Enum):
    """Playlist type."""

    Editorial = "editorial"
    External = "external"
    PersonalMix = "personal-mix"
    Replay = "replay"
    UserShared = "user-shared"


class PlaylistAttributes(BaseModel):
    """Class that represents data about playlist.
    Not meant to be used directly.
    """

    artwork: Artwork = Artwork(**{})
    curator_name: str = Field(alias="curatorName")
    description: Notes = Notes(**{})
    is_chart: bool = Field(alias="isChart")
    has_collaboration: bool = Field(alias="hasCollaboration", default=False)
    last_modified_date: str = Field(
        alias="lastModifiedDate", default="1970-01-01"
    )
    name: str
    playlist_type: PlaylistType = Field(alias="playlistType")
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    supports_sing: bool = Field(alias="supportsSing", default=False)
    track_types: PlaylistTrackTypes = Field(
        alias="trackTypes", default=PlaylistTrackTypes.Undefined
    )
    url: str


class Playlist(AppleMusicObject):
    """Class that represents music playlist.

    Attributes
    ----------
    id: `str`
        Unique playlist ID.
    type: `str`
        Object type. Should be "playlists".
    href: `str`
        Playlist URL.
    artwork: `Artwork`
        Data about playlist artwork. Can be empty.
    curator_name: `str`
        Playlist author name.
    description: `Notes`
        Playlist description. Can be empty.
    is_chart: `bool`
        If playlist is a chart.
    has_collaboration: `bool`
        If playlist is collaborative work.
    last_modified_date: `str`
        Playlist edit date in format YYYY-MM-DD.
    name: `str`
        Playlist name.
    playlist_type: `PlaylistType`
        Playlist type.
    play_params: `PlayParameters`
        Parameters associated with playback.
    supports_sing: `bool`
        If playlist supports Sing function.
    track_types: `PlaylistTrackTypes`
        Playlist track types. Can be undefined.
    url: `str`
        Playlist URL.
    """

    attributes: PlaylistAttributes

    @property
    def artwork(self) -> Artwork:
        return self.attributes.artwork

    @property
    def curator_name(self) -> str:
        return self.attributes.curator_name

    @property
    def description(self) -> Notes:
        return self.attributes.description

    @property
    def is_chart(self) -> bool:
        return self.attributes.is_chart

    @property
    def has_collaboration(self) -> bool:
        return self.attributes.has_collaboration

    @property
    def last_modified_date(self) -> str:
        return self.attributes.last_modified_date

    @property
    def name(self) -> str:
        return self.attributes.name

    @property
    def playlist_type(self) -> PlaylistType:
        return self.attributes.playlist_type

    @property
    def supports_sing(self) -> bool:
        return self.attributes.supports_sing

    @property
    def track_types(self) -> PlaylistTrackTypes:
        return self.attributes.track_types

    @property
    def url(self) -> str:
        return self.attributes.url

    def __str__(self) -> str:
        return f"Playlist {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryPlaylistAttributes(BaseModel):
    """Class that represents data about playlist.
    Not meant to be used directly.
    """

    artwork: Artwork = Artwork(**{})
    can_delete: bool = Field(alias="canDelete", default=False)
    can_edit: bool = Field(alias="canEdit")
    date_added: str = Field(alias="dateAdded", default="1970-01-01")
    description: Notes = Notes(**{})
    has_catalog: bool = Field(alias="hasCatalog")
    has_collaboration: bool = Field(alias="hasCollaboration", default=False)
    is_public: bool = Field(alias="isPublic")
    name: str
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    track_types: PlaylistTrackTypes = Field(
        alias="trackTypes", default=PlaylistTrackTypes.Undefined
    )


class LibraryPlaylist(AppleMusicObject):
    """Class that represents library music playlist.

    Attributes
    ----------
    id: `str`
        Unique playlist ID.
    type: `str`
        Object type. Should be "library-playlists".
    href: `str`
        Playlist URL.
    artwork: `Artwork`
        Data about playlist artwork. Can be empty.
    can_delete: `bool`
        If it's possible to delete the playlist.
    can_edit: `bool`
        If it's possible to edit the playlist.
    date_added: `str`
        Playlist addition date in format YYYY-MM-DD.
    description: `Notes`
        Playlist description. Can be empty.
    has_catalog: `bool`
        If playlist is in Apple Music catalog.
    has_collaboration: `bool`
        If playlist is collaborative work.
    is_public: `bool`
        If playlist is public.
    name: `str`
        Playlist name.
    play_params: `PlayParameters`
        Parameters associated with playback.
    track_types: `PlaylistTrackTypes`
        Playlist track types. Can be undefined.
    """

    attributes: LibraryPlaylistAttributes

    @property
    def artwork(self) -> Artwork:
        return self.attributes.artwork

    @property
    def can_delete(self) -> bool:
        return self.attributes.can_delete

    @property
    def can_edit(self) -> bool:
        return self.attributes.can_edit

    @property
    def date_added(self) -> str:
        return self.attributes.date_added

    @property
    def description(self) -> Notes:
        return self.attributes.description

    @property
    def has_catalog(self) -> bool:
        return self.attributes.has_catalog

    @property
    def has_collaboration(self) -> bool:
        return self.attributes.has_collaboration

    @property
    def is_public(self) -> bool:
        return self.attributes.is_public

    @property
    def name(self) -> str:
        return self.attributes.name

    @property
    def play_params(self) -> PlayParameters:
        return self.attributes.play_params

    @property
    def track_types(self) -> PlaylistTrackTypes:
        return self.attributes.track_types

    def __str__(self) -> str:
        return f"LibraryPlaylist {self.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

    def add_songs(self, songs: list[LibrarySong | Song]) -> bool:
        """`bool`: Adds songs to playlist.

        Needs Music User Token.

        Arguments
        ---------
        songs: list[`LibrarySong`|`Song`]
            A list of songs to be added.
        """
        return self._client.playlist.add_to_playlist(self, songs)

    def list_songs(self) -> list[LibrarySong]:
        """list[`LibrarySong`]: Returns a list of playlist songs."""
        return self._client.playlist.list_tracks(self)

    def remove_songs(self, song: LibrarySong) -> bool:
        """`bool`: Removes song from playlist.

        Needs Music User Token.

        Arguments
        ---------
        song: `LibrarySong`
            A song to be removed.
        """
        return self._client.playlist.delete_from_playlist(self, song)

    def delete(self) -> bool:
        """`bool`: Deletes the playlist.

        Needs Music User Token.
        """
        return self._client.playlist.delete_playlist(self)
