from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING

from applemusic.models.album import Album, LibraryAlbum
from applemusic.models.artist import Artist, LibraryArtist
from applemusic.models.meta import CatalogTypes, LibraryTypes
from applemusic.models.object import AppleMusicObject
from applemusic.models.playlist import LibraryPlaylist, Playlist
from applemusic.models.song import LibrarySong, Song

if TYPE_CHECKING:
    from applemusic.client import ApiClient

_log = logging.getLogger(__name__)


class SortOrder(Enum):
    DateAddedAscending = "dateAdded"  # From old to new
    DateAddedDescending = "-dateAdded"  # From new to old
    NameAscending = "name"  # A-Z
    NameDescending = "-name"  # Z-A


class LibraryAPI:
    """Library related API endpoints."""

    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def songs(
        self, sort: SortOrder = SortOrder.DateAddedDescending, lang="en"
    ) -> list[LibrarySong]:
        """List[`Song`]: Returns a list of library songs.

        Could be slow. Internally limited by 100 songs per request.

        Needs a Music User Token.
        """
        songs = []
        url = "/v1/me/library/songs"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url,
                params={"limit": 100, "sort": sort.value, "l": lang},
            ) as resp:
                js = resp.json()
                _log.debug("songs list response: %s", js)
                for s in js["data"]:
                    song = LibrarySong(self.client, **s)
                    songs.append(song)
                if url := js.get("next", False):
                    pass
                else:
                    return songs

    def search(
        self, query: str, return_type: LibraryTypes, limit: int = 5, lang="en"
    ) -> list[LibrarySong | LibraryAlbum | LibraryArtist | LibraryPlaylist]:
        """List[`LibrarySong`|`LibraryAlbum`|`LibraryArtist`|`LibraryPlaylist`]: Returns search results.
        Returned type is determined by `return_type` parameter.

        Needs a Music User Token.

        Arguments
        ---------
        query: `str`
            Search query.
        return_type: `LibraryTypes`
            What to search for.
        limit: `int`
            Limit for returned results. Can't be more than 25 internally.
        """
        types = [return_type.value]
        results = []
        url = "/v1/me/library/search"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url,
                params={"term": query, "types": types, "limit": 25, "l": lang},
            ) as resp:
                js = resp.json()
                _log.debug("search response: %s", js)
                if js["results"] == {}:
                    return []
                if songs := js["results"].get(LibraryTypes.Songs.value, False):
                    for res in songs["data"]:
                        results.append(LibrarySong(self.client, **res))
                if albums := js["results"].get(
                    LibraryTypes.Albums.value, False
                ):
                    for res in albums["data"]:
                        results.append(LibraryAlbum(self.client, **res))
                if artists := js["results"].get(
                    LibraryTypes.Artists.value, False
                ):
                    for res in artists["data"]:
                        results.append(LibraryArtist(self.client, **res))
                if playlists := js["results"].get(
                    LibraryTypes.Playlists.value, False
                ):
                    for res in playlists["data"]:
                        results.append(LibraryPlaylist(self.client, **res))
                if len(results) >= limit:
                    return results[:limit]
                else:
                    url = js["results"][return_type.value].get("next", None)
                    if url is None:
                        return results

    def add(self, object_to_add: AppleMusicObject) -> bool:
        """`bool`: Adds an object to user's music library.

        Needs a Music User Token.

        Arguments
        ---------
        object_to_add: `AppleMusicObject`
            Object to add to library. Can be either `Song`, `Album`, `Artist` or `Playlist`.
        """
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
            if resp.text != "":
                _log.debug("library add response: %s", resp.json())
            return resp.status_code == 202

    def remove(self, object_to_delete: AppleMusicObject) -> bool:
        """`bool`: Removes an object from user's music library.

        Needs a Music User Token.

        Arguments
        ---------
        object_to_delete: `AppleMusicObject`
            Object to delete from library. Can be either `LibrarySong`,
            `LibraryAlbum`, `LibraryArtist` or `LibraryPlaylist`.
        """
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
            if resp.text != "":
                _log.debug("library remove response: %s", resp.json())
            return resp.status_code == 204

    def favorite(self, object_to_favorite: AppleMusicObject) -> bool:
        """`bool`: Favorites an object in user music library.

        Needs a Music User Token.

        Arguments
        ---------
        object_to_favorite: `AppleMusicObject`
            Object to favorite. Can be either `Song`, `Album`, `Artist` or `Playlist`.
        """
        item_type = None
        match object_to_favorite:
            case Song():
                item_type = CatalogTypes.Songs.value
            case Album():
                item_type = CatalogTypes.Albums.value
            case Artist():
                item_type = CatalogTypes.Artists.value
            case Playlist():
                item_type = CatalogTypes.Playlists.value
        with self.client.session.post(
            self.client.session.base_url + "/v1/me/favorites",
            params={f"ids[{item_type}]": object_to_favorite.id},
        ) as resp:
            if resp.text != "":
                _log.debug("favorites add response: %s", resp.json())
            return resp.status_code == 202

    def unfavorite(self, object_to_delete: AppleMusicObject) -> bool:
        """`bool`: Removes an object from user's favorites.

        Needs a Music User Token.

        Arguments
        ---------
        object_to_delete: `AppleMusicObject`
            Object to delete from favorites. Can be either `Song`, `Album`, `Artist` or `Playlist`.
        """
        item_type = None
        match object_to_delete:
            case Song():
                item_type = CatalogTypes.Songs.value
            case Album():
                item_type = CatalogTypes.Albums.value
            case Artist():
                item_type = CatalogTypes.Artists.value
            case Playlist():
                item_type = CatalogTypes.Playlists.value
        with self.client.session.delete(
            self.client.session.base_url + "/v1/me/favorites",
            params={f"ids[{item_type}]": object_to_delete.id},
        ) as resp:
            if resp.text != "":
                _log.debug("favorites remove response: %s", resp.json())
            return resp.status_code == 204

    def get_corresponding_library_song(
        self, song: Song, fast=True
    ) -> LibrarySong | None:
        """`LibrarySong`|`None`: Returns matching song in user library.

        Needs Music User Token.

        Arguments
        ---------
        song: `Song`
            Song to query library for.
        fast: `bool`
            Use faster query mechanism, but sometimes unreliable.
        """
        if fast:
            songs = self.search(song.artist_name, LibraryTypes.Songs, limit=25)
        else:
            songs = self.songs()
        for library_song in songs:
            if library_song.play_params.catalog_id == song.play_params.id:
                return song
        return None

    def get_by_id(
        self, object_id: str, object_type: LibraryTypes, lang="en"
    ) -> LibrarySong | LibraryAlbum | LibraryArtist | LibraryPlaylist | None:
        url = f"/v1/me/library"
        match object_type:
            case LibraryTypes.Songs:
                url += "/songs"
            case LibraryTypes.Albums:
                url += "/albums"
            case LibraryTypes.Artists:
                url += "/artists"
            case LibraryTypes.Playlists:
                url += "/playlists"
        with self.client.session.get(
            self.client.session.base_url + url + f"/{object_id}",
            params={"l": lang},
        ) as resp:
            js = resp.json()
            _log.debug("get by id response: %s", js)
            if js["data"] == []:
                return None
            match object_type:
                case LibraryTypes.Songs:
                    return LibrarySong(self.client, **js["data"][0])
                case LibraryTypes.Albums:
                    return LibraryAlbum(self.client, **js["data"][0])
                case LibraryTypes.Artists:
                    return LibraryArtist(self.client, **js["data"][0])
                case LibraryTypes.Playlists:
                    return LibraryPlaylist(self.client, **js["data"][0])
            return None

    def get_artwork(self, song: LibrarySong) -> bytes:
        """`bytes`: Returns artwork for song.

        Arguments
        ---------
        song: `LibrarySong`
            Song to get artwork for.
        """
        url = song.artwork.url
        if url == "":
            return b""
        with self.client.session.get(url) as resp:
            return resp.content