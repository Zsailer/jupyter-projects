"""Leverage JupyterHub's database API to avoid building
an incompatible DB from scratch...
"""
import os
import pathlib

from jupyterhub.orm import (
    User,
    Group,
    Base,
    new_session_factory
)
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship


DB_URL = "sqlite:///jupyter_projects.sqlite"

# user:group many:many mapping table
group_project_map = Table(
    'group_project_map',
    Base.metadata,
    Column('groups_id', ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True),
    Column('projects_id', ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True),
)


class Project(Base):
    """The Project table.
    """
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    groups = relationship('Group', secondary='group_project_map', backref='projects')

    def __repr__(self):
        return "<%s %s (%i projects)>" % (
            self.__class__.__name__,
            self.name,
            len(self.groups),
        )

    @classmethod
    def find(cls, db, name):
        """Find a group by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()


def init_db(fname: str, path: str = None):
    if path:
        db_path = pathlib.Path(path) / fname
    else:
        db_path = pathlib.Path(fname)

    if db_path.exists():
        db_path.unlink()

    db_url = f"sqlite:///{db_path}"

    session_factory = new_session_factory(url=db_url)
    db = session_factory()

    users = [
        User(name="Alice", admin=True),
        User(name="Bob", admin=False),
        User(name="Charlie", admin=False),
    ]
    groups = [
        Group(name="group1", users=[users[0], users[1]]),
        Group(name="group2", users=[users[0], users[2]]),
        Group(name="group3", users=[users[1], users[2]]),
    ]
    projects = [
        Project(name="project1", groups=[groups[0], groups[1]]),
        Project(name="project2", groups=[groups[1], groups[2]]),
    ]
    items = users + groups + projects

    for item in items:
        db.add(item)

    db.commit()
    return db