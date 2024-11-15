from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from ._common import Environment, Runner, User, _IdentifiableMixin
from ._types import Datetime


class MergeRequest(BaseModel, _IdentifiableMixin):
    # See merge_request_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    iid: int
    title: str
    source_branch: str
    source_project_id: int
    target_branch: str
    target_project_id: int
    state: str
    merge_status: str
    detailed_merge_status: str
    url: AnyHttpUrl


class ArtifactsFile(BaseModel):
    # See build_hook_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    filename: Optional[str]
    size: Optional[int]


class Build(BaseModel, _IdentifiableMixin):
    # See build_hook_attrs() in
    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/data_builder/pipeline.rb
    stage: str
    name: str
    status: str
    created_at: Datetime
    started_at: Optional[Datetime]
    finished_at: Optional[Datetime]
    duration: Optional[float]
    queued_duration: Optional[float]
    failure_reason: Optional[str]
    when: Optional[str]
    manual: bool
    allow_failure: bool
    user: User
    runner: Optional[Runner]
    artifacts_file: ArtifactsFile
    environment: Optional[Environment]
