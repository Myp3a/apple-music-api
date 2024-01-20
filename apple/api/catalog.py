from enum import Enum

from apple.models.album import Album
from apple.models.artist import Artist
from apple.models.object import AppleMusicObject
from apple.models.playlist import Playlist
from apple.models.song import Song


class CatalogTypes(Enum):
    Activities = "activities"
    Albums = "albums"
    AppleCurators = "apple-curators"
    Artists = "artists"
    Curators = "curators"
    MusicVideos = "music-videos"
    Playlists = "playlists"
    RecordLabels = "record-labels"
    Songs = "songs"
    Stations = "stations"

class CatalogAPI:
    def __init__(self, client) -> None:
        self.client = client
        # TODO: make dynamic storefront detection
        self.storefront = "ru"

    def search(self, query, return_type: CatalogTypes, limit=5) -> list[AppleMusicObject]:
        types = [return_type.value]
        query = query.replace(" ", "+")
        results = []
        next = True
        url = f"/v1/catalog/{self.storefront}/search"
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
                if (songs := js["results"].get(CatalogTypes.Songs.value, False)):
                    for res in songs["data"]:
                        results.append(Song(**res))
                if (albums := js["results"].get(CatalogTypes.Albums.value, False)):
                    for res in albums["data"]:
                        results.append(Album(**res))
                if (artists := js["results"].get(CatalogTypes.Artists.value, False)):
                    for res in artists["data"]:
                        results.append(Artist(**res))
                if (playlists := js["results"].get(CatalogTypes.Playlists.value, False)):
                    for res in playlists["data"]:
                        results.append(Playlist(**res))
                if len(results) >= limit:
                    return results[:limit]
                else:
                    url = js["results"][return_type.value].get("next", None)
                    if url is None:
                        return results
