from enum import Enum

from apple.api.catalog import CatalogTypes
from apple.models.album import LibraryAlbum, Album
from apple.models.artist import LibraryArtist, Artist
from apple.models.object import AppleMusicObject
from apple.models.playlist import LibraryPlaylist, Playlist
from apple.models.song import LibrarySong, Song


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
        next = True
        url = "/v1/me/library/songs"
        while next:
            with self.client.session.get(self.client.session.base_url + url) as resp:
                js = resp.json()
                for s in js["data"]:
                    song = LibrarySong(**s)
                    songs.append(song)
                if url := js.get("next", False):
                    next = True
                else:
                    next = False
                    return songs

    def search(self, query, return_type: LibraryTypes, limit=5) -> list[AppleMusicObject]:
        types = [return_type.value]
        query = query.replace(" ", "+")
        results = []
        next = True
        url = "/v1/me/library/search"
        while next:
            with self.client.session.get(
                self.client.session.base_url + url,
                params={
                    "term": query,
                    "types": types,
                    "limit": 25
                    }
            ) as resp:
                js = resp.json()
                if js["results"] == {}:
                    return []
                if (songs := js["results"].get(LibraryTypes.Songs.value, False)):
                    for res in songs["data"]:
                        results.append(LibrarySong(**res))
                if (albums := js["results"].get(LibraryTypes.Albums.value, False)):
                    for res in albums["data"]:
                        results.append(LibraryAlbum(**res))
                if (artists := js["results"].get(LibraryTypes.Artists.value, False)):
                    for res in artists["data"]:
                        results.append(LibraryArtist(**res))
                if (playlists := js["results"].get(LibraryTypes.Playlists.value, False)):
                    for res in playlists["data"]:
                        results.append(LibraryPlaylist(**res))
                if len(results) >= limit:
                    return results[:limit]
                else:
                    url = js["results"][return_type.value].get("next", None)
                    if url is None:
                        return results
                    
    def add(self, object_to_add) -> bool:
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
            params={
                f"ids[{item_type}]": object_to_add.id
            }
        ) as resp:
            print(resp.text)
            if resp.status_code == 202:
                return True
            else:
                return False
