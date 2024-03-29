from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from applemusic.models.meta import CatalogTypes, LibraryTypes
from applemusic.models.playlist import LibraryPlaylist, Playlist
from applemusic.models.song import LibrarySong, Song

if TYPE_CHECKING:
    from applemusic.client import ApiClient

_log = logging.getLogger(__name__)


class PlaylistAPI:
    """Playlist related API endpoints."""

    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def list_playlists(self) -> list[LibraryPlaylist]:
        """List[`Playlist`]: Returns a list of library playlists.

        Internally limited by 25 playlists per request.

        Needs a Music User Token.
        """
        playlists = []
        url = "/v1/me/library/playlists"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url
            ) as resp:
                js = resp.json()
                _log.debug("playlist list response: %s", js)
                for p in js["data"]:
                    playlist = LibraryPlaylist(self.client, **p)
                    playlists.append(playlist)
                if url := js.get("next", False):
                    pass
                else:
                    return playlists

    def create_playlist(
        self, name: str, description: str = ""
    ) -> LibraryPlaylist | bool:
        """`LibraryPlaylist`|`False`: Creates a new playlist and returns it.
        Otherwise returns `False`.

        Needs a Music User Token.

        Arguments
        ---------
        name: `str`
            Name for new playlist.
        description: `str`
            Description for new playlist.
        """
        url = "/v1/me/library/playlists"
        with self.client.session.post(
            self.client.session.base_url + url,
            json={
                "attributes": {"name": name, "description": description},
                "relationships": {"tracks": {"data": []}},
            },
        ) as resp:
            js = resp.json()
            _log.debug("create playlist response: %s", js)
            if resp.status_code == 201:
                return LibraryPlaylist(self.client, **resp.json()["data"][0])
            else:
                return False

    def delete_playlist(self, playlist: LibraryPlaylist) -> bool:
        """`bool`: Deletes a playlist from library.

        Needs a Music User Token.

        Arguments
        ---------
        playlist: `LibraryPlaylist`
            Playlist to delete.
        """
        with self.client.session.delete(
            self.client.session.base_url
            + f"/v1/me/library/playlists/{playlist.id}"
        ) as resp:
            if resp.text != "":
                _log.debug("delete playlist response: %s", resp.json())
            return resp.status_code == 204

    def add_to_playlist(
        self, playlist: LibraryPlaylist, songs: list[Song | LibrarySong]
    ) -> bool:
        """`bool`: Adds songs to playlist.

        Needs a Music User Token.

        Arguments
        ---------
        playlist: `LibraryPlaylist`
            Playlist to add songs to.
        songs: List[`Song`|`LibrarySong`]
            List of songs to add to playlist.
        """
        tracks_to_add = []
        for s in songs:
            t = None
            if isinstance(s, Song):
                t = CatalogTypes.Songs.value
            elif isinstance(s, LibrarySong):
                t = LibraryTypes.Songs.value
            tracks_to_add.append({"type": t, "id": s.id})
        with self.client.session.post(
            self.client.session.base_url
            + f"/v1/me/library/playlists/{playlist.id}/tracks",
            json={"data": tracks_to_add},
        ) as resp:
            if resp.text != "":
                _log.debug("add to playlist response: %s", resp.json())
            return resp.status_code == 201

    def delete_from_playlist(
        self, playlist: LibraryPlaylist, song: LibrarySong
    ) -> bool:
        """`bool`: Adds songs to playlist.

        Needs a Music User Token.

        Arguments
        ---------
        playlist: `LibraryPlaylist`
            Playlist to add songs to.
        song: `LibrarySong`
            Song to remove from playlist.
        """
        with self.client.session.delete(
            self.client.session.base_url
            + f"/v1/me/library/playlists/{playlist.id}/tracks",
            params={"ids[library-songs]": song.id, "mode": "all"},
        ) as resp:
            js = resp.json()
            if resp.text != "":
                _log.debug("remove from playlist response: %s", js)
            return resp.status_code == 204

    def list_tracks(
        self, playlist: LibraryPlaylist | Playlist
    ) -> list[Song | LibrarySong]:
        """List[`LibrarySong`|`Song`]: Returns a list of library songs.

        Internally limited by 100 songs per request.
        """
        res = []
        if isinstance(playlist, LibraryPlaylist):
            url = f"/v1/me/library/playlists/{playlist.id}/tracks"
        elif isinstance(playlist, Playlist):
            url = f"/v1/catalog/{self.client.storefront}/playlists/{playlist.id}/tracks"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url
            ) as resp:
                js = resp.json()
                _log.debug("playlist tracks response: %s", js)
                tracks = js["data"]
                for t in tracks:
                    match t["type"]:
                        case "library-songs":
                            track = LibrarySong(self.client, **t)
                        case "songs":
                            track = Song(self.client, **t)
                    res.append(track)
                if url := js.get("next", False):
                    pass
                else:
                    return res

    def in_playlist(
        self, playlist: LibraryPlaylist | Playlist, song: LibrarySong | Song
    ) -> bool:
        """`bool`: If song is in specified playlist.

        Could be slow.

        Arguments
        ---------
        playlist: `LibraryPlaylist`|`Playlist`
            Playlist to search in.
        song: `LibrarySong`|`Song`
            Song to search for.
        """
        tracks = self.list_tracks(playlist)
        for t in tracks:
            if t.id == song.id:
                return True
        return False
