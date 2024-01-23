import re

from pydantic import BaseModel, Field

from applemusic.models.meta import PlayParameters
from applemusic.models.object import AppleMusicObject


class LyricsAttributes(BaseModel):
    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    ttml: str


class Lyrics(AppleMusicObject):
    attributes: LyricsAttributes

    def __str__(self) -> str:
        return self.clean

    def __repr__(self) -> str:
        return f"<{self.__str__()} ({self.id})>"

    @property
    def ttml(self) -> str:
        return self.attributes.ttml

    @property
    def clean(self) -> str:
        lyrics_lines = re.findall(r"(?:<p.*?>)(.*?)(?:</p>)", self.ttml)
        return "\n".join(lyrics_lines)
