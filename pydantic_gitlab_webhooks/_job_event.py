from typing import Optional

from pydantic import BaseModel

from ._common import _IdentifiableMixin
from ._types import Datetime


class Commit(BaseModel, _IdentifiableMixin):
    name: str
    sha: str
    message: str
    author_name: str
    author_email: str
    status: str
    duration: Optional[float] = None
    started_at: Optional[Datetime] = None
    finished_at: Optional[Datetime] = None
