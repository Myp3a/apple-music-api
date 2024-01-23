import logging
from enum import Enum

from applemusic.models.meta import Subscription

_log = logging.getLogger(__name__)


class MetaKeys(Enum):
    """Meta keys that can be requested."""

    Subscription = "subscription"


class AccountAPI:
    """Account related API endpoints."""

    def __init__(self, client) -> None:
        self.client = client

    def subscription(self) -> Subscription:
        """`Subscription`: Represents current user subscription data.

        Needs a Music User Token.
        """
        with self.client.session.get(
            self.client.session.base_url + "/v1/me/account",
            params={"meta": MetaKeys.Subscription.value},
        ) as resp:
            js = resp.json()
            _log.debug("subscription response: %s", js)
            return Subscription(**js["meta"]["subscription"])
