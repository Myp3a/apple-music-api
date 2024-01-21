import logging

from enum import Enum

from apple.models.meta import Subscription


_log = logging.getLogger(__name__)

class MetaKeys(Enum):
    Subscription = "subscription"

class AccountAPI:
    def __init__(self, client) -> None:
        self.client = client

    def subscription(self):
        with self.client.session.get(self.client.session.base_url + "/v1/me/account",
                                     params={
                                         "meta": MetaKeys.Subscription.value
                                     }
        ) as resp:
            js = resp.json()
            _log.debug("subscription response: %s", js)
            return Subscription(**js["meta"]["subscription"])
