from typing import Literal, Optional

from pydantic import BaseModel

from ._common import Commit, Label
from ._common import MergeRequest as BaseMergeRequest
from ._common import User
from ._types import Change


class MergeRequest(BaseMergeRequest):
    action: (
        Literal["open"]
        | Literal["close"]
        | Literal["reopen"]
        | Literal["update"]
        | Literal["approved"]
        | Literal["unapproved"]
        | Literal["approval"]
        | Literal["unapproval"]
        | Literal["merge"]
    )
    oldrev: Optional[str] = None


class Changes(BaseModel):
    target_branch: Optional[Change[str]] = None
    source_branch: Optional[Change[str]] = None
    assignee_id: Optional[Change[Optional[int]]] = None
    title: Optional[Change[Optional[str]]] = None
    milestone_id: Optional[Change[Optional[int]]] = None
    state: Optional[Change[str]] = None
    merge_status: Optional[Change[str]] = None
    description: Optional[Change[Optional[str]]] = None
    labels: Optional[Change[Optional[list[Label]]]] = None
    last_commit: Optional[Change[Optional[Commit]]] = None
    draft: Optional[Change[bool]] = None
    assignee: Optional[Change[Optional[User]]] = None
    detailed_merge_status: Optional[Change[str]] = None
