from pydantic import AnyHttpUrl, BaseModel


class Link(BaseModel):
    id: int
    link_type: str
    name: str
    url: AnyHttpUrl


class Source(BaseModel):
    format: str
    url: AnyHttpUrl


class Assets(BaseModel):
    count: int
    links: list[Link]
    sources: list[Source]
