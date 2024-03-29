import re

from pydantic import BaseModel, Field

from applemusic.models.meta import PlayParameters
from applemusic.models.object import AppleMusicObject


class LyricsAttributes(BaseModel):
    """Class that represents lyrics data.
    Not meant to be used directly.
    """

    play_params: PlayParameters = Field(
        alias="playParams", default=PlayParameters(**{})
    )
    ttml: str


class Lyrics(AppleMusicObject):
    """Class that represents lyrics.

    Attributes
    ----------
    id: `str`
        Unique artist ID.
    type: `str`
        Object type. Should be "lyrics".
    play_params: `PlayParameters`
        Parameters associated with playback.
    ttml: `str`
        TTML-encoded lyrics.
    """

    attributes: LyricsAttributes

    @property
    def play_params(self) -> PlayParameters:
        return self.attributes.play_params

    def __str__(self) -> str:
        return self.clean

    def __repr__(self) -> str:
        return f"<Lyrics ({self.id})>"

    @property
    def ttml(self) -> str:
        """`str`: Lyrics in TTML format."""
        return self.attributes.ttml

    @property
    def clean(self) -> str:
        """`str`: Lyrics in clean format."""
        lyrics_lines = re.findall(r"(?:<p.*?>)(.*?)(?:</p>)", self.ttml)
        return "\n".join(lyrics_lines)
