from typing import Literal, Optional

from pydantic import AnyHttpUrl, BaseModel, EmailStr

from ._types import Date, Datetime

# The GitLab documentation for webhook event bodies is at:
#   https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html
#
# In cases where this is insufficiently precise, the source code which generates the hooks can be
# found at:
#   https://gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/data_builder
# or:
#   https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data


class _TimestampedMixin:
    "Mixin class for resources with GitLab-style created and updated at timestamps"
    created_at: Datetime
    updated_at: Datetime


class _IdentifiableMixin:
    "Mixin class for resources with optional numeric ids"
    id: Optional[int] = None


class StDiff(BaseModel):
    diff: str
    new_path: str
    old_path: str
    a_mode: str
    b_mode: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool


class Note(BaseModel, _TimestampedMixin, _IdentifiableMixin):
    # See: https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/note_builder.rb
    #
    # attachment is always null (https://gitlab.com/gitlab-org/gitlab/-/issues/17303) and so is
    # omitted. Similarly other attributes which are only ever null on
    # https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html are omitted until
    # their expected value types are documented.
    note: str
    noteable_type: str
    author_id: int
    project_id: int
    line_code: Optional[str]
    commit_id: Optional[str] = None
    noteable_id: Optional[int]
    system: bool
    st_diff: Optional[StDiff] = None
    action: Optional[str] = None
    url: AnyHttpUrl


class Label(BaseModel, _TimestampedMixin, _IdentifiableMixin):
    # See "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/label.rb
    title: str
    color: str
    project_id: Optional[int]
    template: bool
    description: Optional[str]
    type: str
    group_id: Optional[int]


class UserNameAndEmail(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr | Literal["[REDACTED]"]] = None


class User(UserNameAndEmail, _IdentifiableMixin):
    # See "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/user.rb
    #
    # name and username are marked as optional since the GitLab docs[1] have examples where they
    # are absent.
    #
    # [1] https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html
    username: Optional[str] = None
    avatar_url: Optional[AnyHttpUrl] = None


class Project(BaseModel, _IdentifiableMixin):
    # See "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/project.rb
    name: str
    description: str
    web_url: str
    avatar_url: Optional[AnyHttpUrl] = None
    git_ssh_url: str
    git_http_url: AnyHttpUrl
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: Optional[str] = None


class Issue(BaseModel, _TimestampedMixin, _IdentifiableMixin):
    # See: https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/issue_builder.rb
    title: str
    assignee_ids: list[int]
    assignee_id: Optional[int]
    author_id: int
    project_id: int
    position: Optional[int] = None
    description: str
    milestone_id: Optional[int]
    state: str
    iid: int
    labels: list[Label]


class CommitAuthor(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    # See: "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/commit.rb
    id: str
    message: str = ""
    title: str = ""
    timestamp: Datetime
    url: AnyHttpUrl
    author: CommitAuthor


class MergeRequest(BaseModel, _TimestampedMixin, _IdentifiableMixin):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/merge_request_builder.rb
    target_branch: str
    source_branch: str
    source_project_id: int
    author_id: int
    assignee_id: Optional[int]
    title: str
    milestone_id: Optional[int]
    state: str
    merge_status: str
    target_project_id: int
    iid: int
    description: str
    position: Optional[int] = None
    labels: list[Label]
    source: Optional[Project]
    target: Optional[Project]
    last_commit: Commit
    draft: bool
    assignee: Optional[User] = None
    detailed_merge_status: str


class Snippet(BaseModel, _TimestampedMixin, _IdentifiableMixin):
    # See "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/snippet.rb
    title: str
    description: str
    content: str
    author_id: int
    project_id: int
    file_name: str
    type: str
    visibility_level: int
    url: AnyHttpUrl


class Wiki(BaseModel):
    # See "hook_attrs" in https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/wiki.rb
    web_url: AnyHttpUrl
    git_ssh_url: str
    git_http_url: AnyHttpUrl
    path_with_namespace: str
    default_branch: str


class WikiPage(BaseModel):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/wiki_page_builder.rb
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/models/wiki_page.rb
    title: str
    content: str
    format: str
    message: str
    slug: str
    url: AnyHttpUrl
    action: str
    diff_url: AnyHttpUrl
    version_id: str


class PipelineVariable(BaseModel):
    key: str
    value: str


class Pipeline(BaseModel, _IdentifiableMixin):
    # See "hook_attrs()" in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    iid: int
    name: str
    ref: str
    tag: bool
    sha: str
    before_sha: str
    source: str
    status: str
    stages: list[str]
    created_at: Datetime
    finished_at: Datetime
    duration: int
    variables: list[PipelineVariable]
    url: AnyHttpUrl


class SourcePipelineProject(BaseModel, _IdentifiableMixin):
    # See source_pipeline_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    web_url: AnyHttpUrl
    path_with_namespace: str


class SourcePipeline(BaseModel):
    # See source_pipeline_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    project: SourcePipelineProject
    pipeline_id: int
    job_id: int


class Runner(BaseModel, _IdentifiableMixin):
    # See runner_hook_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    description: str
    active: bool
    runner_type: str
    is_shared: bool
    tags: Optional[list[str]] = None


class Environment(BaseModel):
    # See environment_hook_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    name: str
    action: str
    deployment_tier: Optional[str] = None


class FeatureFlag(BaseModel, _IdentifiableMixin):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/feature_flag.rb
    name: str
    description: Optional[str] = None
    active: bool


class EmojiAward(BaseModel, _IdentifiableMixin, _TimestampedMixin):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/emoji_builder.rb
    user_id: int
    name: str
    awardable_type: Optional[str] = None
    awardable_id: Optional[int] = None
    action: str
    awarded_on_url: AnyHttpUrl


class AccessToken(BaseModel, _IdentifiableMixin):
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/hook_data/resource_access_token_builder.rb
    user_id: int
    created_at: Datetime
    name: str
    expires_at: Date
