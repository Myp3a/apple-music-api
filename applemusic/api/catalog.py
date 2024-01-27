import logging
from enum import Enum

from applemusic.models.album import Album
from applemusic.models.artist import Artist
from applemusic.models.lyrics import Lyrics
from applemusic.models.playlist import Playlist
from applemusic.models.song import Song

_log = logging.getLogger(__name__)


class CatalogTypes(Enum):
    """Available catalog search types."""

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
    """Catalog related API endpoints."""

    def __init__(self, client) -> None:
        self.client = client

    def search(
        self, query: str, return_type: CatalogTypes, limit: int = 5
    ) -> list[Song | Album | Artist | Playlist]:
        """List[`Song`|`Album`|`Artist`|`Playlist`]: Returns search results.
        Returned type is determined by `return_type` parameter.

        Arguments
        ---------
        query: `str`
            Search query.
        return_type: `CatalogTypes`
            What to search for.
        limit: `int`
            Limit for returned results. Can't be more than 25 internally.
        """
        types = [return_type.value]
        results = []
        url = f"/v1/catalog/{self.client.storefront}/search"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url,
                params={"term": query, "types": types, "limit": 25},
            ) as resp:
                js = resp.json()
                _log.debug("search response: %s", js)
                if js["results"] == {}:
                    return []
                if songs := js["results"].get(CatalogTypes.Songs.value, False):
                    for res in songs["data"]:
                        results.append(Song(**res))
                if albums := js["results"].get(
                    CatalogTypes.Albums.value, False
                ):
                    for res in albums["data"]:
                        results.append(Album(**res))
                if artists := js["results"].get(
                    CatalogTypes.Artists.value, False
                ):
                    for res in artists["data"]:
                        results.append(Artist(**res))
                if playlists := js["results"].get(
                    CatalogTypes.Playlists.value, False
                ):
                    for res in playlists["data"]:
                        results.append(Playlist(**res))
                if len(results) >= limit:
                    return results[:limit]
                url = js["results"][return_type.value].get("next", None)
                if url is None:
                    return results

    def lyrics(self, song: Song) -> Lyrics | None:
        """`Lyrics`: Returns lyrics for song.

        Arguments
        ---------
        song: `Song`
            Catalog song to search lyrics for.
        """
        with self.client.session.get(
            self.client.session.base_url
            + f"/v1/catalog/{self.client.storefront}/songs/{song.id}/lyrics"
        ) as resp:
            js = resp.json()
            _log.debug("lyrics response: %s", js)
            if js["data"] == []:
                return None
            return Lyrics(**js["data"][0])

    def get_by_id(self, song_id: str) -> Song | None:
        """`Song`: Returns a song by it's id.

        Arguments
        ---------
        song_id: `str`
            Song ID to search for.
        """
        with self.client.session.get(
            self.client.session.base_url
            + f"/v1/catalog/{self.client.storefront}/songs/{song_id}"
        ) as resp:
            js = resp.json()
            _log.debug("get by id response: %s", js)
            if js["data"] == []:
                return None
            return Song(**js["data"][0])

    def get_by_isrc(self, isrc: str) -> Song | None:
        """`Song`: Returns a song by it's ISRC.

        Arguments
        ---------
        isrc: `str`
            ISRC to search for.
        """
        with self.client.session.get(
            self.client.session.base_url
            + f"/v1/catalog/{self.client.storefront}/songs",
            params={"filter[isrc]": isrc},
        ) as resp:
            js = resp.json()
            _log.debug("get by isrc response: %s", js)
            if js["data"] == []:
                return None
            return Song(**js["data"][0])
