from __future__ import annotations

import base64
import io
import logging
from typing import TYPE_CHECKING

import m3u8
from pywidevine import PSSH, Cdm, Device
from pywidevine.license_protocol_pb2 import WidevinePsshData

from applemusic.decrypt import decrypt
from applemusic.models.song import Song

if TYPE_CHECKING:
    from applemusic.client import ApiClient

_log = logging.getLogger(__name__)


class PlaybackAPI:
    """Playlist related API endpoints.
    WARNING: More hacky than other parts of the API! Can break at any time.
    ty https://github.com/glomatico/gamdl !
    """

    def __init__(self, client: ApiClient) -> None:
        self.client = client
        self.playback_url = (
            "https://play.itunes.apple.com/WebObjects/MZPlay.woa/wa/webPlayback"
        )
        self.license_url = "https://play.itunes.apple.com/WebObjects/MZPlay.woa/wa/acquireWebPlaybackLicense"
        self.default_flavor = "28:ctrp256"
        try:
            self.cdm = Cdm.from_device(
                Device.load(self.client.widevine_device_path)
            )
            self.cdm_session = self.cdm.open()
        except FileNotFoundError:
            _log.warning(
                "No Widevine Device File found, audio downloads will be"
                " unavailable"
            )

    def get_webplayback(self, song: Song) -> dict:
        """`dict`: Returns a song object with playback streams.

        Needs a Music User Token.
        """
        with self.client.session.post(
            self.playback_url,
            json={
                "salableAdamId": song.play_params.id,
                "language": "en-US",
            },
        ) as resp:
            js = resp.json()
            _log.debug("webplayback response: %s", js)
            error = js.get("failureType", False)
            # TODO: Raise a meaningful error
            assert error is False, "Error getting webplayback info"
            return js["songList"][0]

    def get_available_streams(self, song: Song) -> dict[str, str]:
        """`dict`: Returns a dictionary of song_format: m3u8_url.

        Needs a Music User Token.
        """
        result = {}
        data = self.get_webplayback(song)
        for asset in data["assets"]:
            result[asset["flavor"]] = asset["URL"]
        _log.debug("available streams: %s", result)
        return result

    def get_license(self, challenge: str, track_url: str, track_id: str) -> str:
        """`str`: Returns a base64 encoded license key for track.

        Needs a Music User Token.
        """
        with self.client.session.post(
            self.license_url,
            json={
                "challenge": challenge,
                "key-system": "com.widevine.alpha",
                "uri": track_url,
                "adamId": track_id,
                "isLibrary": False,
                "user-initiated": True,
            },
        ) as resp:
            js = resp.json()
            _log.debug("get license response: %s", js)
            assert js["status"] == 0, "Error getting license"
            return js["license"]

    def get_decryption_key(self, track_url: str, track_id: str) -> bytes:
        """`bytes`: Returns a key for track.

        Needs a Widevine device file.
        """
        playlist = m3u8.load(track_url)
        key_url = str(playlist.keys[0].uri)
        key = base64.b64decode(key_url.split(",")[1])
        pssh_data = WidevinePsshData()
        pssh_data.algorithm = 1
        pssh_data.key_ids.append(key)
        pssh = PSSH(base64.b64encode(pssh_data.SerializeToString()).decode())
        challenge = base64.b64encode(
            self.cdm.get_license_challenge(self.cdm_session, pssh)
        ).decode()
        license_b64 = self.get_license(challenge, key_url, track_id)
        self.cdm.parse_license(self.cdm_session, license_b64)
        return next(
            key
            for key in self.cdm.get_keys(self.cdm_session)
            if key.type == "CONTENT"
        ).key

    def get_encrypted_audio_with_key(self, song: Song) -> tuple[bytes, bytes]:
        """(`bytes`,`bytes`): Returns tuple of raw encrypted music data and decryption key.

        Needs a Music User Token.

        Needs a Widevine device file.
        """
        track_id = song.play_params.id
        flavors = self.get_available_streams(song)
        url = flavors[self.default_flavor]
        key = self.get_decryption_key(url, track_id)
        playlist = m3u8.load(url)
        path = url.replace(url.split("/")[-1], "") + "/"
        part_url = playlist.segments[0]
        with self.client.session.get(path + part_url.uri) as resp:
            return resp.content, key

    def get_decrypted_audio(self, song: Song) -> bytes:
        """`bytes`: Returns raw decrypted music data.

        Needs a Music User Token.

        Needs a Widevine device file.
        """
        encrypted, key = self.get_encrypted_audio_with_key(song)
        inp_buf = io.BytesIO()
        out_buf = io.BytesIO()
        inp_buf.write(encrypted)
        inp_buf.seek(0)
        decrypt(key, inp_buf, out_buf)
        out_buf.seek(0)
        return out_buf.getbuffer()
