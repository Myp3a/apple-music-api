import requests
import time

from apple.api.account import AccountAPI
from apple.api.catalog import CatalogAPI
from apple.api.library import LibraryAPI
from apple.api.playlist import PlaylistAPI


class Session:
    def __init__(self, dev_token, user_token) -> None:
        self.session = requests.Session()
        self.session.headers["origin"] = "https://music.apple.com"
        self.session.headers["Authorization"] = f"Bearer {dev_token}"
        self.session.headers["Music-User-Token"] = user_token
        self.base_url = "https://amp-api.music.apple.com"

    def get(self, *args, **kwargs) -> requests.Response:
        done = False
        while not done:
            with self.session.get(*args, **kwargs) as resp:
                if resp.status_code == 429:
                    print("Too many requests, waiting")
                    time.sleep(1)
                else:
                    done = True
                    return resp

    def post(self, *args, **kwargs) -> requests.Response:
        done = False
        while not done:
            with self.session.post(*args, **kwargs) as resp:
                if resp.status_code == 429:
                    print("Too many requests, waiting")
                    time.sleep(1)
                else:
                    done = True
                    return resp

    def delete(self, *args, **kwargs) -> requests.Response:
        done = False
        while not done:
            with self.session.delete(*args, **kwargs) as resp:
                if resp.status_code == 429:
                    print("Too many requests, waiting")
                    time.sleep(1)
                else:
                    done = True
                    return resp

class ApiClient:
    def __init__(self, developer_token, user_token) -> None:
        self.developer_token = developer_token
        self.user_token = user_token
        self.session = Session(self.developer_token, self.user_token)
        self.library = LibraryAPI(self)
        self.catalog = CatalogAPI(self)
        self.playlist = PlaylistAPI(self)
        self.account = AccountAPI(self)
        self.storefront = self.account.subscription().storefront
