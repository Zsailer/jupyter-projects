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
async def create_project(request: Request, project: ProjectModel):
    db = router.app.db
    # Convert request model to ORM object.
    project_orm = project.to_orm()
    # Add to database
    db.add(project_orm)
    db.commit()


@router.delete(
    '/api/projects/{name}',
)
async def delete_project(request: Request, name: str):
    db = router.app.db
    project = Project.find(db=db, name=name)
    db.delete(project)
    db.commit()