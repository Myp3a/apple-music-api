from enum import Enum
from pydantic import BaseModel, Field

from apple.models.meta import Artwork, PlayParameters
from apple.models.object import AppleMusicObject


class PlaylistTrackTypes(Enum):
    Undefined = None
    MusicVideos = "music-videos"
    Songs = "songs"

class PlaylistType(Enum):
    Editorial = "editorial"
    External = "external"
    PersonalMix = "personal-mix"
    Replay = "replay"
    UserShared = "user-shared"

class PlaylistDescription(BaseModel):
    standard: str = ""
    short: str = ""

class PlaylistAttributes(BaseModel):
    artwork: Artwork = Artwork(**{})
    curator_name: str = Field(alias="curatorName")
    description: PlaylistDescription = PlaylistDescription(**{})
    is_chart: bool = Field(alias="isChart")
    last_modified_date: str = Field(alias="lastModifiedDate", default="1970-01-01")
    name: str
    playlist_type: PlaylistType = Field(alias="playlistType")
    play_params: PlayParameters = Field(alias="playParams", default=PlayParameters(**{}))
    track_types: PlaylistTrackTypes = Field(alias="trackTypes", default=PlaylistTrackTypes.Undefined)
    url: str

class Playlist(AppleMusicObject):
    attributes: PlaylistAttributes

    def __str__(self) -> str:
        return f"Playlist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibraryPlaylistAttributes(BaseModel):
    artwork: Artwork = Artwork(**{})
    can_edit: bool = Field(alias="canEdit")
    date_added: str = Field(alias="dateAdded", default="1970-01-01")
    description: PlaylistDescription = PlaylistDescription(**{})
    has_catalog: bool = Field(alias="hasCatalog")
    is_public: bool = Field(alias="isPublic")
    name: str
    play_params: PlayParameters = Field(alias="playParams", default=PlayParameters(**{}))
    track_types: PlaylistTrackTypes = Field(alias="trackTypes", default=PlaylistTrackTypes.Undefined)

class LibraryPlaylist(AppleMusicObject):
    attributes: LibraryPlaylistAttributes

    def __str__(self) -> str:
        return f"LibraryPlaylist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
