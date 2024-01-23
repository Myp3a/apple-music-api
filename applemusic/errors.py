from pydantic import BaseModel


class ErrorSource(BaseModel):
    parameter: str = ""
    pointer: str = ""


class AppleMusicAPIException(Exception):
    """Base exception class for Apple Music API.

    Attributes
    ----------
    code: int
        HTTP error code?
    detail: str
        Detailed error description, if available.
    id: str
        Unique Apple error ID.
    source: ErrorSource
        Detailed information about position of error.
    status: int
        HTTP error code.
    title: str
        Short error message.
    """

    def __init__(self, data, *args: object) -> None:
        super().__init__(*args)
        self.code = data.get("code")
        self.detail = data.get("detail", "No detailed description available")
        self.id = data.get("id")
        self.source = ErrorSource(**data.get("source", {}))
        self.status = data.get("status")
        self.title = data.get("title")

    def __str__(self):
        text = self.title
        if self.detail != "No detailed description available":
            text += f": {self.detail}"
        return f"{text}"
