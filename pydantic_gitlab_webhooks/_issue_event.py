from typing import Literal, Optional

from pydantic import BaseModel

from ._common import Issue as BaseIssue
from ._common import Label
from ._types import Change


class Issue(BaseIssue):
    action: Literal["open"] | Literal["close"] | Literal["reopen"] | Literal["update"]


class Changes(BaseModel):
    title: Optional[Change[Optional[str]]] = None
    assignee_ids: Optional[Change[Optional[list[int]]]] = None
    assignee_id: Optional[Change[Optional[int]]] = None
    description: Optional[Change[Optional[str]]] = None
    milestone_id: Optional[Change[Optional[int]]] = None
    state: Optional[Change[str]] = None
    labels: Optional[Change[Optional[list[Label]]]] = None
