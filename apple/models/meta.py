from enum import Enum


class Artwork:
    def __init__(self, data) -> None:
        self.width = data.get("width", 0)
        self.height = data.get("height", 0)
        self.url = data.get("url", "")

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

class PlayParameters():
    def __init__(self, data) -> None:
        self.id = data.get("id")
        self.kind = data.get("kind")
        self.is_library = data.get("isLibrary")
        self.reporting = data.get("reporting")
        self.catalog_id = data.get("catalogId")
        self.reporting_id = data.get("reportingId")
