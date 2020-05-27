import pathlib
import importlib

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

import uvicorn


from .db import init_db

HERE = pathlib.Path(__file__).resolve()
HERE_DIR = HERE.parent
# TEMPLATE_DIR = HERE_DIR / "templates"
# templates = Jinja2Templates(directory=TEMPLATE_DIR)

def main():

    app = FastAPI(
        title="Jupyter Projects",
        description="Multiple people under a single Jupyter workspace, writing notebooks together"
    )

    db = init_db()

    ROUTERS = [
        'api'
    ]

    # Hook up routers found in this module.
    for router in ROUTERS:
        mod = importlib.import_module('jupyter_projects.' + router)
        mod.router.app = app
        mod.router.db = db
        app.include_router(mod.router)

    uvicorn.run(app)



if __name__ == "__main__":
    main()

