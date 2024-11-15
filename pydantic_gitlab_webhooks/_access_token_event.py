from pydantic import BaseModel


class Group(BaseModel):
    group_name: str
    group_path: str
    group_id: int
    full_path: str
