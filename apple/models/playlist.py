from enum import Enum

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

class PlaylistDescription:
    def __init__(self, data) -> None:
        self.standard = data.get("standard", "")
        self.short = data.get("short", "")

class PlaylistAttributes:
    def __init__(self, data) -> None:
        self.artwork = Artwork(data.get("artwork", {}))
        self.curator_name = data.get("curatorName")
        self.description = PlaylistDescription(data.get("description", {}))
        self.is_chart = data.get("isChart")
        self.last_modified_date = data.get("lastModifiedDate","1970-01-01")
        self.name = data.get("name")
        self.playlist_type = PlaylistType(data.get("playlistType"))
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.track_types = PlaylistTrackTypes(data.get("trackTypes", None))
        self.url = data.get("url")

class Playlist(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = PlaylistAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"Playlist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

class LibraryPlaylistAttributes:
    def __init__(self, data) -> None:
        self.artwork = Artwork(data.get("artwork", {}))
        self.can_edit = data.get("canEdit")
        self.date_added = data.get("dateAdded", "1970-01-01")
        self.description = PlaylistDescription(data.get("description", {}))
        self.has_catalog = data.get("hasCatalog")
        self.is_public = data.get("isPublic")
        self.name = data.get("name")
        self.play_params = PlayParameters(data.get("playParams",{}))
        self.track_types = PlaylistTrackTypes(data.get("trackTypes", None))

class LibraryPlaylist(AppleMusicObject):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.attributes = LibraryPlaylistAttributes(data.get("attributes"))

    def __str__(self) -> str:
        return f"LibraryPlaylist {self.attributes.name}"

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"
