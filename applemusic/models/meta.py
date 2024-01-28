from enum import Enum

from pydantic import BaseModel, Field


class Artwork(BaseModel):
    """Data about artwork.

    Attributes
    ----------
    width: `int`
        Width in pixels. Can be undefined.
    height: `int`
        Height in pixels. Can be undefined.
    url: `str`
        Artwork URL. Can be empty.
    """

    width: int | None = 0
    height: int | None = 0
    url: str = ""


class AudioVariants(Enum):
    """Available audio qualities."""

    Atmos = "atmos"
    DolbyAtmos = "dolby-atmos"
    DolbyAudio = "dolby-audio"
    HiResLossless = "hi-res-lossless"
    Lossless = "lossless"
    LossyStereo = "lossy-stereo"
    Spatial = "spatial"
    Surround = "surround"


class CatalogTypes(Enum):
    """Available catalog search types."""

    Activities = "activities"
    Albums = "albums"
    AppleCurators = "apple-curators"
    Artists = "artists"
    Curators = "curators"
    MusicVideos = "music-videos"
    Playlists = "playlists"
    RecordLabels = "record-labels"
    Songs = "songs"
    Stations = "stations"


class ContentRating(Enum):
    """Content rating of element."""

    No = "no"
    Clean = "clean"
    Explicit = "explicit"


class LibraryTypes(Enum):
    """Available library search types."""

    Albums = "library-albums"
    Artists = "library-artists"
    MusicVideos = "library-music-videos"
    Playlists = "library-playlists"
    Songs = "library-songs"


class Notes(BaseModel):
    """Notes about object.

    Attributes
    ----------
    name: `str`
        Name of note. Can be empty.
    short: `str`
        Short note. Can be empty.
    standard: `str`
        More descriptive note. Can be empty.
    tagline: `str`
        Note tagline. Can be empty.
    """

    name: str = ""
    short: str = ""
    standard: str = ""
    tagline: str = ""


class PlayParameters(BaseModel):
    """Playback related parameters.

    Attributes
    ----------
    id: `str`
        Unique element ID.
    kind: `str`
        Element type.
    is_library: `bool`
        If object is from library.
    reporting: `bool`
        ?
    catalog_id: `str`
        ID of element in catalog search.
    reporting_id: `str`
        ?
    """

    id: str = ""
    kind: str = ""
    is_library: bool = Field(alias="isLibrary", default=False)
    reporting: bool = False
    catalog_id: str = Field(alias="catalogId", default="")
    reporting_id: str = Field(alias="reportingId", default="")


class Subscription(BaseModel):
    active: bool
    storefront: str
