from enum import Enum
from pydantic import BaseModel, Field

class Artwork(BaseModel):
    width: int = 0
    height: int = 0
    url: str = ""

class AudioVariants(Enum):
    Undefined = None
    DolbyAtmos = "dolby-atmos"
    DolbyAudio = "dolby-audio"
    HiResLossless = "hi-res-lossless"
    Lossless = "lossless"
    LossyStereo = "lossy-stereo"

class ContentRating(Enum):
    No = "no"
    Clean = "clean"
    Explicit = "explicit"

class PlayParameters(BaseModel):
    id: str = ""
    kind: str = ""
    is_library: bool = Field(alias="isLibrary", default=False)
    reporting: bool = False
    catalog_id: str = Field(alias="catalogId", default="")
    reporting_id: str = Field(alias="reportingId", default="")
