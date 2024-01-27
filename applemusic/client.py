import logging
import time
from functools import wraps

import requests

from applemusic.api.account import AccountAPI
from applemusic.api.catalog import CatalogAPI
from applemusic.api.library import LibraryAPI
from applemusic.api.playback import PlaybackAPI
from applemusic.api.playlist import PlaylistAPI
from applemusic.errors import AppleMusicAPIException

_log = logging.getLogger(__name__)


class Session:
    """Wrapper for requests.Session. Provides authentication, error and ratelimit handling.

    Arguments
    ---------
    dev_token: str
        Apple Developer token.
    user_token: str | None
        Music User Token for library interaction.
    verify_ssl: bool
        SSL verification for debug purposes.

    Methods
    -------
    get: requests.Response
        requests.get() wrapper.
    post: requests.Response
        requests.post() wrapper.
    delete: requests.Response
        requests.delete() wrapper.
    """

    def __init__(self, dev_token, user_token, verify_ssl) -> None:
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers["origin"] = "https://music.apple.com"
        self.session.headers["Authorization"] = f"Bearer {dev_token}"
        self.session.headers["Music-User-Token"] = user_token
        self.base_url = "https://amp-api.music.apple.com"

    def _request(self, func, *args, **kwargs) -> requests.Response:  # type: ignore
        # TODO: drop out of loop if waiting for too long
        done = False
        while not done:
            _log.debug("Doing network request with %s", func)
            with func(*args, **kwargs) as resp:
                _log.debug("Got response with code %s", resp.status_code)
                if resp.status_code == 429:
                    _log.warning("Got ratelimited, sleeping a bit")
                    time.sleep(1)
                elif resp.status_code >= 400:
                    error = resp.json()["errors"][0]
                    raise AppleMusicAPIException(error)
                else:
                    done = True
                    return resp

    @wraps(requests.get)
    def get(self, *args, **kwargs) -> requests.Response:
        return self._request(self.session.get, *args, **kwargs)

    @wraps(requests.post)
    def post(self, *args, **kwargs) -> requests.Response:
        return self._request(self.session.post, *args, **kwargs)

    @wraps(requests.delete)
    def delete(self, *args, **kwargs) -> requests.Response:
        return self._request(self.session.delete, *args, **kwargs)


class ApiClient:
    """Represents a client connection that connects to Apple Music API.
    This class is used to interact with API.

    Parameters
    ----------
    developer_token: str
        Apple Developer token.
    user_token: str | None
        Music User Token for library interaction.
        If None, only free API will be available.
    widevine_device_path: str
        Widevine Device File for media decryption.
        If doesn't exist, audio downloads will be unavailable.
    storefront: str | None
        Specific storefront for catalog requests. Auto-detects by default.
    verify_ssl: bool
        SSL verification for debug purposes.

    Attributes
    ----------
    storefront: str
        Two-letter encoded country of Apple storefront location
    session: applemusic.Session
        Wrapper for requests.Session with authentication, error and ratelimit handling.
    library: applemusic.LibraryAPI
        Library API endpoints client
    catalog: applemusic.CatalogAPI
        Catalog API endpoints client
    playlist: applemusic.PlaylistAPI
        Playlist API endpoints client
    account: applemusic.AccountAPI
        Account API endpoints client
    playback: applemusic.PlaybackAPI
        Playback API endpoints client
    """

    def __init__(
        self,
        developer_token,
        user_token=None,
        widevine_device_path="device.wvd",
        storefront=None,
        verify_ssl=True,
    ) -> None:
        self.developer_token = developer_token
        self.user_token = user_token
        self.widevine_device_path = widevine_device_path
        self.session = Session(
            self.developer_token, self.user_token, verify_ssl
        )
        self.library = LibraryAPI(self)
        self.catalog = CatalogAPI(self)
        self.playlist = PlaylistAPI(self)
        self.account = AccountAPI(self)
        self.playback = PlaybackAPI(self)
        if self.user_token:
            if storefront is None:
                self.storefront = self.account.subscription().storefront
            else:
                self.storefront = storefront
        else:
            _log.warning(
                "No Music User Token provided, library functions unavailable"
            )
            assert (
                storefront is not None
            ), "Provide either Music User Token or storefront"
            self.storefront = storefront
