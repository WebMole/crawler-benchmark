import matplotlib

matplotlib.use('Agg')

import os
import tempfile

import pytest

import project


@pytest.fixture
def client():
    db_fd, project.app.config['DATABASE'] = tempfile.mkstemp()
    project.app.config['TESTING'] = True
    client = project.app.test_client()

    with project.app.app_context():
        project.init_db()

    yield client

    os.close(db_fd)
    os.unlink(project.app.config['DATABASE'])


def test_home(client):
    rv = client.get('/')
    assert rv._status_code == 200
