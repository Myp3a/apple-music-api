from pydantic import BaseModel


class AppleMusicObject(BaseModel):
    id: str
    type: str
    href: str
    attributes: str
    relationships: dict = {}
    views: dict = {}
