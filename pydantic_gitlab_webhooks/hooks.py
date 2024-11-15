from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter

from .events import (
    AnyAccessTokenEvent,
    AnyEvent,
    AnyNoteEvent,
    DeploymentEvent,
    EmojiEvent,
    FeatureFlagEvent,
    GroupMemberEvent,
    IssueEvent,
    JobEvent,
    MergeRequestEvent,
    PipelineEvent,
    ProjectEvent,
    PushEvent,
    ReleaseEvent,
    SubgroupEvent,
    TagPushEvent,
    WikiPageEvent,
)


class _DeploymentHook(BaseModel):
    header: Literal["Deployment Hook"]
    event_body: DeploymentEvent


class _EmojiHook(BaseModel):
    header: Literal["Emoji Hook"]
    event_body: EmojiEvent


class _FeatureFlagHook(BaseModel):
    header: Literal["Feature Flag Hook"]
    event_body: FeatureFlagEvent


class _IssueHook(BaseModel):
    header: Literal["Issue Hook"]
    event_body: IssueEvent


class _JobHook(BaseModel):
    header: Literal["Job Hook"]
    event_body: JobEvent


class _MemberHook(BaseModel):
    header: Literal["Member Hook"]
    event_body: GroupMemberEvent


class _MergeRequestHook(BaseModel):
    header: Literal["Merge Request Hook"]
    event_body: MergeRequestEvent


class _NoteHook(BaseModel):
    header: Literal["Note Hook"]
    event_body: AnyNoteEvent


class _PipelineHook(BaseModel):
    header: Literal["Pipeline Hook"]
    event_body: PipelineEvent


class _ProjectHook(BaseModel):
    header: Literal["Project Hook"]
    event_body: ProjectEvent


class _PushHook(BaseModel):
    header: Literal["Push Hook"]
    event_body: PushEvent


class _TagPushHook(BaseModel):
    header: Literal["Tag Push Hook"]
    event_body: TagPushEvent


class _ReleaseHook(BaseModel):
    header: Literal["Release Hook"]
    event_body: ReleaseEvent


class _AccessTokenHook(BaseModel):
    header: Literal["Resource Access Token Hook"]
    event_body: AnyAccessTokenEvent


class _SubgroupHook(BaseModel):
    header: Literal["Subgroup Hook"]
    event_body: SubgroupEvent


class _WikiPageHook(BaseModel):
    header: Literal["Wiki Page Hook"]
    event_body: WikiPageEvent


_AnyHook = Annotated[
    Union[
        _AccessTokenHook,
        _DeploymentHook,
        _EmojiHook,
        _FeatureFlagHook,
        _IssueHook,
        _JobHook,
        _MemberHook,
        _MergeRequestHook,
        _NoteHook,
        _PipelineHook,
        _ProjectHook,
        _PushHook,
        _ReleaseHook,
        _SubgroupHook,
        _TagPushHook,
        _WikiPageHook,
    ],
    Field(discriminator="header"),
]

_HOOK_VALIDATOR = TypeAdapter(_AnyHook)


def validate_event_header_and_body(header: str, body: dict) -> AnyEvent:
    """
    Validate an event header body against the webhook schema.

    Args:
        header: Value of the X-Gitlab-Event header
        body: Python dictionary representing the received event body

    Returns:
        a validated and parsed event
    """
    return _HOOK_VALIDATOR.validate_python({"header": header, "event_body": body}).event_body
