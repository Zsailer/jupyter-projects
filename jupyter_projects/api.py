from fastapi import APIRouter, Request
from jupyterhub.orm import User, Group
from .db import Project
from .models import (
    UserModel,
    GroupModel,
    ProjectModel,
    ProjectListModel
)

# Initialize the API Router for Projects REST API.
router = APIRouter()


@router.get(
    '/api/projects',
    response_model=ProjectListModel
)
def list_projects(request: Request):
    """Get a list of projects.
    """
    projects = [ProjectModel.from_orm(p) for p in router.db.query(Project)]
    return ProjectListModel(projects=projects)


@router.get(
    '/api/projects/{name}',
    response_model=ProjectModel
)
def get_named_project_details(request: Request, name: str):
    """Get a list of projects.
    """
    project = Project.find(db=router.db, name=name)
    return ProjectModel.from_orm(project)
