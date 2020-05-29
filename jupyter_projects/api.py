from fastapi import APIRouter, Request
from jupyterhub.orm import User, Group
from .db import Project
from .models import (
    UserModel,
    GroupModel,
    GroupListModel,
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
    """List projects that are currently
    """
    projects = [ProjectModel.from_orm(p) for p in router.app.db.query(Project)]
    return ProjectListModel(projects=projects)


@router.get(
    '/api/projects/{name}',
    response_model=ProjectModel
)
def get_project_model(request: Request, name: str):
    """Get a list of projects.
    """
    project = Project.find(db=router.app.db, name=name)
    return ProjectModel.from_orm(project)


@router.post(
    '/api/projects',
)
def create_project(request: Request, project: ProjectModel):
    db = router.app.db
    # Convert request model to ORM object.
    project_orm = project.to_orm()
    # Add to database
    db.add(project_orm)
    db.commit()


@router.delete(
    '/api/projects/{name}',
)
def delete_project(request: Request, name: str):
    """Delete the project with the given name."""
    db = router.app.db
    project = Project.find(db=db, name=name)
    db.delete(project)
    db.commit()


@router.get(
    '/api/projects/{name}/groups',
    response_model=GroupListModel
)
def get_groups_in_project(request: Request, name: str):
    """"""
    project_orm = Project.find(db=router.app.db, name=name)
    project_model = ProjectModel.from_orm(project_orm)
    return GroupListModel(groups=project_model.groups)


@router.post(
    '/api/projects/{name}/groups/{group_name}',
)
def add_group_to_project(request: Request, name: str, group_name: str):
    """
    """
