from typing import Annotated, Literal, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, Field

from . import (
    _access_token_event,
    _issue_event,
    _job_event,
    _merge_request_event,
    _pipeline_event,
    _release_event,
)
from ._common import (
    AccessToken,
    Commit,
    EmojiAward,
    Environment,
    FeatureFlag,
    Issue,
    Label,
    MergeRequest,
    Note,
    Pipeline,
    Project,
    Runner,
    Snippet,
    SourcePipeline,
    User,
    UserNameAndEmail,
    Wiki,
    WikiPage,
)
from ._types import Datetime

__all__ = [
    "AnyEvent",
    "CommitNoteEvent",
    "DeploymentEvent",
    "EmojiEvent",
    "FeatureFlagEvent",
    "GroupAccessTokenEvent",
    "GroupMemberEvent",
    "IssueEvent",
    "IssueNoteEvent",
    "JobEvent",
    "MergeRequestNoteEvent",
    "PipelineEvent",
    "ProjectAccessTokenEvent",
    "ProjectEvent",
    "PushEvent",
    "ReleaseEvent",
    "SnippetNoteEvent",
    "SubgroupEvent",
    "TagPushEvent",
    "WikiPageEvent",
]


class _BasePushEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/push.rb
    before: Optional[str] = None
    after: Optional[str] = None
    ref: Optional[str] = None
    ref_protected: bool
    checkout_sha: str
    user_id: int
    user_name: Optional[str] = None
    user_username: Optional[str] = None
    user_email: Optional[str] = None
    user_avatar: Optional[AnyHttpUrl] = None
    project_id: int
    project: Project
    commits: list[Commit]
    total_commits_count: int


class PushEvent(_BasePushEvent):
    object_kind: Literal["push"]
    event_name: Literal["push"]


class TagPushEvent(_BasePushEvent):
    object_kind: Literal["tag_push"]
    event_name: Literal["tag_push"]


class IssueEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/issue_builder.rb
    object_kind: Literal["issue"] | Literal["work_item"]
    # all the docs say is 'the object_kind field is work_item, and the type is the work item type.'
    event_type: str
    user: User
    project: Project
    object_attributes: _issue_event.Issue
    assignees: Optional[list[User]] = None
    assignee: Optional[User] = None
    labels: Optional[list[Label]] = None
    changes: Optional[_issue_event.Changes] = None


class _BaseNoteEvent(BaseModel):
    # See: https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/note.rb
    #
    # Note: "repository" is deprecated and is omitted.
    object_kind: Literal["note"]
    event_type: Literal["note"] | Literal["confidential_note"]
    user: User
    project_id: int
    project: Project
    object_attributes: Note


class CommitNoteEvent(_BaseNoteEvent):
    commit: Commit


class IssueNoteEvent(_BaseNoteEvent):
    issue: Issue


class MergeRequestNoteEvent(_BaseNoteEvent):
    merge_request: MergeRequest


class SnippetNoteEvent(_BaseNoteEvent):
    snippet: Snippet


AnyNoteEvent = Union[CommitNoteEvent, IssueNoteEvent, MergeRequestNoteEvent, SnippetNoteEvent]


class MergeRequestEvent(BaseModel):
    # TODO: work out where this is defined in the GitLab source code.
    object_kind: Literal["merge_request"]
    event_type: Literal["merge_request"]
    user: User
    project: Project
    object_attributes: _merge_request_event.MergeRequest
    labels: Optional[list[Label]] = None
    assignees: Optional[list[User]] = None
    reviewers: Optional[list[User]] = None
    changes: Optional[_merge_request_event.Changes] = None


class WikiPageEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/wiki_page.rb
    object_kind: Literal["wiki_page"]
    user: User
    project: Project
    wiki: Wiki
    object_attributes: WikiPage


class PipelineEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    object_kind: Literal["pipeline"]
    object_attributes: Pipeline
    merge_request: Optional[_pipeline_event.MergeRequest] = None
    user: User
    project: Project
    commit: Commit
    source_pipeline: Optional[SourcePipeline] = None
    builds: list[_pipeline_event.Build]


class JobEvent(BaseModel):
    # TODO: work out where this is defined in the GitLab source code.
    object_kind: Literal["build"]
    ref: Optional[str] = None
    tag: bool
    before_sha: Optional[str] = None
    sha: str
    build_id: int
    build_name: str
    build_stage: str
    build_status: str
    build_created_at: Optional[Datetime] = None
    build_started_at: Optional[Datetime] = None
    build_finished_at: Optional[Datetime] = None
    build_duration: Optional[float] = None
    build_queued_duration: Optional[float] = None
    build_allow_failure: bool
    build_failure_reason: Optional[str] = None
    retries_count: int
    pipeline_id: int
    project_id: int
    project_name: str
    user: User
    commit: _job_event.Commit
    project: Project
    runner: Runner
    environment: Optional[Environment] = None
    source_pipeline: SourcePipeline


class DeploymentEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/deployment.rb
    object_kind: Literal["deployment"]
    status: str
    status_changed_at: Optional[Datetime] = None
    deployment_id: int
    deployable_id: int
    deployable_url: AnyHttpUrl
    environment: Optional[str] = None
    environment_tier: Optional[str] = None
    environment_slug: Optional[str] = None
    # Environment external URLs are provided by users and so may not actually be URLs(!)
    environment_external_url: Optional[str] = None
    project: Project
    short_sha: str
    user: User
    user_url: AnyHttpUrl
    commit_url: AnyHttpUrl
    commit_title: str


class GroupMemberEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/group_member_builder.rb
    created_at: Datetime
    updated_at: Datetime
    group_name: str
    group_path: str
    group_id: int
    user_username: str
    user_name: str
    user_email: str
    user_id: int
    group_access: str
    expires_at: Datetime
    event_name: (
        Literal["user_update_for_group"]
        | Literal["user_add_to_group"]
        | Literal["user_remove_from_group"]
        | Literal["user_access_request_to_group"]
        | Literal["user_access_request_denied_for_group"]
    )


class ProjectEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/project_member_builder.rb
    event_name: Literal["project_create"] | Literal["project_destroy"]
    created_at: Datetime
    updated_at: Datetime
    name: str
    path: str
    path_with_namespace: str
    project_id: int
    project_namespace_id: int
    owners: list[UserNameAndEmail]
    project_visibility: str


class SubgroupEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/subgroup_builder.rb
    created_at: Datetime
    updated_at: Datetime
    event_name: Literal["subgroup_create"] | Literal["subgroup_destroy"]
    name: str
    path: str
    full_path: str
    group_id: int
    parent_group_id: int
    parent_name: str
    parent_path: str
    parent_full_path: str


class FeatureFlagEvent(BaseModel):
    object_kind: Literal["feature_flag"]
    project: Project
    user: User
    user_url: AnyHttpUrl
    object_attributes: FeatureFlag


class ReleaseEvent(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/release_builder.rb
    object_kind: Literal["release"]
    id: int
    created_at: Datetime
    description: str
    name: str
    released_at: Datetime
    tag: str
    project: Project
    url: AnyHttpUrl
    action: str
    assets: _release_event.Assets
    commit: Commit


class EmojiEvent(BaseModel):
    object_kind: Literal["emoji"]
    event_type: str
    user: User
    project_id: int
    project: Project
    object_attributes: EmojiAward
    note: Note
    issue: Issue


class _BaseAccessTokenEvent(BaseModel):
    object_kind: Literal["access_token"]
    object_attributes: AccessToken
    event_name: str


class ProjectAccessTokenEvent(_BaseAccessTokenEvent):
    project: Project


class GroupAccessTokenEvent(_BaseAccessTokenEvent):
    group: _access_token_event.Group


AnyAccessTokenEvent = Union[ProjectAccessTokenEvent | GroupAccessTokenEvent]


# As an optimisation, group those types which can be matched solely based on a single literal field
# together so that we don't need to try so hard to match things.
_AnyKindDiscriminatedEvent = Annotated[
    Union[
        PushEvent,
        TagPushEvent,
        IssueEvent,
        MergeRequestEvent,
        WikiPageEvent,
        PipelineEvent,
        JobEvent,
        DeploymentEvent,
        FeatureFlagEvent,
        EmojiEvent,
        ReleaseEvent,
    ],
    Field(discriminator="object_kind"),
]

_AnyEventNameDiscriminatedEvent = Annotated[
    Union[
        GroupMemberEvent,
        ProjectEvent,
        SubgroupEvent,
    ],
    Field(discriminator="event_name"),
]


# The ordering of the union is important here, we start with the easiest models to early-out and
# move to models where we need to examine progressively closer.
_AnyParseableEvent = Annotated[
    Union[
        _AnyKindDiscriminatedEvent,
        _AnyEventNameDiscriminatedEvent,
        AnyNoteEvent,
        AnyAccessTokenEvent,
    ],
    Field(union_mode="left_to_right"),
]

# A version of _AnyEvent optimised for type-checking and not for parsing.
AnyEvent = Union[
    CommitNoteEvent,
    DeploymentEvent,
    EmojiEvent,
    FeatureFlagEvent,
    GroupAccessTokenEvent,
    GroupMemberEvent,
    IssueEvent,
    IssueNoteEvent,
    JobEvent,
    MergeRequestNoteEvent,
    MergeRequestEvent,
    PipelineEvent,
    ProjectAccessTokenEvent,
    ProjectEvent,
    PushEvent,
    ReleaseEvent,
    SnippetNoteEvent,
    SubgroupEvent,
    TagPushEvent,
    WikiPageEvent,
]
