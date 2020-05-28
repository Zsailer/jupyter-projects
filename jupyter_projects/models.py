from pydantic import BaseModel, Field
from typing import List, Any
import datetime


class ORMModel(BaseModel):
    class Config:
        orm_mode=True


class UserModel(ORMModel):
    id: int = ...
    name: str = ...
    admin: bool = ...
    created: datetime.datetime = None
    last_activity: datetime.datetime = None
    api_tokens: List[str] = []
    cookie_id: str = None
    encrypted_auth_state: dict = None


class GroupModel(ORMModel):
    id: int = ...
    name: str = ...
    users: List[UserModel]


class ProjectModel(ORMModel):
    id: int = ...
    name: str = ...
    groups: List[GroupModel]


class ProjectListModel(BaseModel):
    projects: List[ProjectModel]