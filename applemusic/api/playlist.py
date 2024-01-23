from applemusic.api.catalog import CatalogTypes
from applemusic.api.library import LibraryTypes
from applemusic.models.playlist import LibraryPlaylist, Playlist
from applemusic.models.song import LibrarySong, Song


class PlaylistAPI:
    def __init__(self, client) -> None:
        self.client = client

    def list_playlists(self) -> list[LibraryPlaylist]:
        playlists = []
        url = "/v1/me/library/playlists"
        while True:
            with self.client.session.get(
                self.client.session.base_url + url
            ) as resp:
                js = resp.json()
                for p in js["data"]:
                    playlist = LibraryPlaylist(**p)
                    playlists.append(playlist)
                if url := js.get("next", False):
                    pass
                else:
                    return playlists

    def create_playlist(self, name, description="") -> LibraryPlaylist | bool:
        url = "/v1/me/library/playlists"
        with self.client.session.post(
            self.client.session.base_url + url,
            json={
                "attributes": {"name": name, "description": description},
                "relationships": {"tracks": {"data": []}},
            },
        ) as resp:
            if resp.status_code == 201:
                return LibraryPlaylist(**resp.json()["data"][0])
            else:
                return False

    def delete_playlist(self, playlist: LibraryPlaylist) -> bool:
        with self.client.session.delete(
            self.client.session.base_url
            + f"/v1/me/library/playlists/{playlist.id}"
        ) as resp:
            return resp.status_code == 204

    def add_to_playlist(
        self, playlist: LibraryPlaylist, songs: list[Song | LibrarySong]
    ) -> bool:
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
            return resp.status_code == 201

    def list_tracks(
        self, playlist: LibraryPlaylist | Playlist
    ) -> list[Song | LibrarySong]:
        res = []
        if isinstance(playlist, LibraryPlaylist):
            url = f"/v1/me/library/playlists/{playlist.id}/tracks"
        elif isinstance(playlist, Playlist):
            url = f"/v1/catalog/{self.client.storefront}/playlists/{playlist.id}/tracks"
        with self.client.session.get(
            self.client.session.base_url + url
        ) as resp:
            js = resp.json()
            tracks = js["data"]
            for t in tracks:
                match t["type"]:
                    case "library-songs":
                        track = LibrarySong(**t)
                    case "songs":
                        track = Song(**t)
                res.append(track)
            return res
