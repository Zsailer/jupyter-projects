from fastapi import APIRouter, Request

from .models import ProjectList, Project
from jupyterhub.orm import User, Group


router = APIRouter()


@router.get('/api/projects')
def list_projects(request: Request):
    """Get a list of projects.
    """
    return


@router.get('/api/projects/{name}')
def get_named_project_details(request: Request, name: str):
    """Get a list of projects.
    """
    group = Group.find(db=router.db, name=name)
    return {"users": group.users}

