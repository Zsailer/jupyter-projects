import pytest

from jupyter_projects.app import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def db_path(tmp_path):
    return tmp_path

@pytest.fixture
def app(db_path):
    return create_app(db_path=db_path)

@pytest.fixture
def client(app):
    return TestClient(app)

def test_list_projects(client):
    response = client.get('/api/projects')
    data = response.json()
    assert response.status_code == 200
    assert 'projects' in data
    assert len(data['projects']) > 1