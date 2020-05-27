"""Leverage JupyterHub's database API to avoid building
an incompatible DB from scratch...
"""
import os
from jupyterhub import orm

DB_URL = "sqlite:///jupyter_projects.sqlite"


def init_db():
    fname = 'jupyter_projects.sqlite'
    if os.path.exists(fname):
        os.remove(fname)

    session_factory = orm.new_session_factory(url=DB_URL)
    db = session_factory()

    users = [
        orm.User(name="Alice", admin=True),
        orm.User(name="Bob", admin=False),
        orm.User(name="Charlie", admin=False),
    ]
    groups = [
        orm.Group(name="group1", users=[users[0], users[1]]),
        orm.Group(name="group2", users=[users[0], users[2]]),
        orm.Group(name="group3", users=[users[1], users[2]]),
    ]
    items = users + groups

    for item in items:
        db.add(item)

    db.commit()
    return db