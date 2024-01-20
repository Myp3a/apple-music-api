class AppleMusicObject:
    def __init__(self, data) -> None:
        self.id = data.get("id")
        self.type = data.get("type")
        self.href = data.get("href")
        self.attributes = data.get("attributes")
        self.relationships = data.get("relationships", {})
        self.views = data.get("views", {})
