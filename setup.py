
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jupyter_projects",
    version="0.0.1",
    author="The Jupyter Team",
    author_email="",
    description="Jupyter Projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires = [
        'pydantic',
        'fastapi',
        'jupyterhub',
        'uvicorn'
    ],
    extras_require = {
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'jupyter-projects = jupyter_projects.app:main'
        ]
    },
    python_requires='>=3.6',
)