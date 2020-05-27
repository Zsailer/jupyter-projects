from pydantic import BaseModel, Field
from typing import List


class Project(BaseModel):
    name: str
    groups: List
    users: List


class ProjectList(BaseModel):
    projects: List[Project]