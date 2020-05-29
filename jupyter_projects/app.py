import pathlib
import importlib

from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from typing import List, Any

from pydantic import (
    BaseModel,
    Field,
    FilePath
)


import uvicorn


from .db import init_db

HERE = pathlib.Path(__file__).resolve()
HERE_DIR = HERE.parent


class JupyterProjectsApplication(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    title: str = "Jupyter Projects"
    description: str = "Multiple people under a single Jupyter workspace, writing notebooks together"
    router_names: List[str] = ['api']
    routers: List = []
    webapp: Any = None
    db: Any = None

    db_path: FilePath = Field(
        default='',
        description="The path to the Jupyter Project Database",
        config=True
    )

    port: int = Field(
        8888,
        description="The port on which to run the server.",
        config=True
    )

    def init_db(self):
        self.db = init_db(fname='jupyter_projects.sqlite', path=self.db_path)

    def init_routers(self):
        # Hook up routers found in this module.
        for router_name in self.router_names:
            mod = importlib.import_module('jupyter_projects.' + router_name)
            router = mod.router
            router.app = self
            self.routers.append(mod.router)

    def init_webapp(self):
        # Initialize the FastaAPI Web Application
        self.webapp = FastAPI(
            title=self.title,
            description=self.description,

        )
        # Append Routers.
        for router in self.routers:
            self.webapp.include_router(router)

    def initialize(self):
        self.init_db()
        self.init_routers()
        self.init_webapp()

    def start(self):
        uvicorn.run(self.webapp, port=self.port)

    @classmethod
    def launch_instance(cls):
        app = cls()
        app.initialize()
        app.start()


main = JupyterProjectsApplication.launch_instance


if __name__ == "__main__":
    main()

