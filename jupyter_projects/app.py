import pathlib
import importlib

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

import uvicorn


from .db import init_db

HERE = pathlib.Path(__file__).resolve()
HERE_DIR = HERE.parent


def create_app(db_path=None):
    app = FastAPI(
        title="Jupyter Projects",
        description="Multiple people under a single Jupyter workspace, writing notebooks together"
    )

    db = init_db(fname='jupyter_projects.sqlite', path=db_path)

    ROUTERS = [
        'api'
    ]

    # Hook up routers found in this module.
    for router in ROUTERS:
        mod = importlib.import_module('jupyter_projects.' + router)
        mod.router.app = app
        mod.router.db = db
        app.include_router(mod.router)

    return app


def main():
    app = create_app()
    uvicorn.run(app)



if __name__ == "__main__":
    main()

