from enum import Enum

from pydantic import BaseModel, Field

from applemusic.models.meta import Artwork, Notes, PlayParameters
from applemusic.models.object import AppleMusicObject


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

    Attributes
    ----------
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
    attributes: `PlaylistAttributes`
        Playlist data.
    """

    attributes: PlaylistAttributes

    def __str__(self) -> str:
        return f"Playlist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"


class LibraryPlaylistAttributes(BaseModel):
    """Class that represents data about playlist.

    Attributes
    ----------
    artwork: `Artwork`
        Data about playlist artwork. Can be empty.
    can_delete: `bool`
        If it's possible to delete the playlist.
    can_edit: `Notes`
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
    attributes: `PlaylistAttributes`
        Playlist data.
    """

    attributes: LibraryPlaylistAttributes

    def __str__(self) -> str:
        return f"LibraryPlaylist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
