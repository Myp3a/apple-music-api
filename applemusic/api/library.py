import logging
from enum import Enum

from apple.api.catalog import CatalogTypes
from apple.models.album import Album, LibraryAlbum
from apple.models.artist import Artist, LibraryArtist
from apple.models.object import AppleMusicObject
from apple.models.playlist import LibraryPlaylist, Playlist
from apple.models.song import LibrarySong, Song

_log = logging.getLogger(__name__)


class LibraryTypes(Enum):
    Albums = "library-albums"
    Artists = "library-artists"
    MusicVideos = "library-music-videos"
    Playlists = "library-playlists"
    Songs = "library-songs"


class LibraryAPI:
    def __init__(self, client) -> None:
        self.client = client

    def songs(self) -> list[LibrarySong]:
        songs = []
        url = "/v1/me/library/songs"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url
            ) as resp:
                js = resp.json()
                _log.debug("songs list response: %s", js)
                for s in js["data"]:
                    song = LibrarySong(**s)
                    songs.append(song)
                if url := js.get("next", False):
                    pass
                else:
                    return songs

    def search(
        self, query: str, return_type: LibraryTypes, limit: int = 5
    ) -> list[LibrarySong | LibraryAlbum | LibraryArtist | LibraryPlaylist]:
        types = [return_type.value]
        query = query.replace(" ", "+")
        results = []
        url = "/v1/me/library/search"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url,
                params={"term": query, "types": types, "limit": 25},
            ) as resp:
                js = resp.json()
                _log.debug("search response: %s", js)
                if js["results"] == {}:
                    return []
                if songs := js["results"].get(LibraryTypes.Songs.value, False):
                    for res in songs["data"]:
                        results.append(LibrarySong(**res))
                if albums := js["results"].get(
                    LibraryTypes.Albums.value, False
                ):
                    for res in albums["data"]:
                        results.append(LibraryAlbum(**res))
                if artists := js["results"].get(
                    LibraryTypes.Artists.value, False
                ):
                    for res in artists["data"]:
                        results.append(LibraryArtist(**res))
                if playlists := js["results"].get(
                    LibraryTypes.Playlists.value, False
                ):
                    for res in playlists["data"]:
                        results.append(LibraryPlaylist(**res))
                if len(results) >= limit:
                    return results[:limit]
                else:
                    url = js["results"][return_type.value].get("next", None)
                    if url is None:
                        return results

    def add(self, object_to_add: AppleMusicObject) -> bool:
        item_type = None
        match object_to_add:
            case Song():
                item_type = CatalogTypes.Songs.value
            case Album():
                item_type = CatalogTypes.Albums.value
            case Artist():
                item_type = CatalogTypes.Artists.value
            case Playlist():
                item_type = CatalogTypes.Playlists.value
        with self.client.session.post(
            self.client.session.base_url + "/v1/me/library",
            params={f"ids[{item_type}]": object_to_add.id},
        ) as resp:
            _log.debug("library add response: %s", resp.json())
            if resp.status_code == 202:
                return True
            else:
                return False

    def remove(self, object_to_delete: AppleMusicObject) -> bool:
        item_type = None
        match object_to_delete:
            case LibrarySong():
                item_type = CatalogTypes.Songs.value
            case LibraryAlbum():
                item_type = CatalogTypes.Albums.value
            case LibraryArtist():
                item_type = CatalogTypes.Artists.value
            case LibraryPlaylist():
                item_type = CatalogTypes.Playlists.value
        with self.client.session.delete(
            self.client.session.base_url
            + f"/v1/me/library/{item_type}/{object_to_delete.id}"
        ) as resp:
            _log.debug("library remove response: %s", resp.json())
            if resp.status_code == 204:
                return True
            else:
                return False
