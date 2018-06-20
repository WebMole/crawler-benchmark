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
    response = client.get('/')
    assert response._status_code == 200


def test_blog(client):
    response = client.get('/modes/blog/')
    assert response._status_code == 200


def test_forum(client):
    response = client.get('/modes/forum/')
    assert response._status_code == 200


def test_newsfeed(client):
    response = client.get('/modes/newsfeed/')
    assert response._status_code == 200


def test_forms(client):
    response = client.get('/modes/forms/')
    assert response._status_code == 200


def test_catalog(client):
    response = client.get('/modes/catalog/')
    assert response._status_code == 200


def test_errors(client):
    response = client.get('/trap/errors/')
    assert response._status_code == 200


def test_random(client):
    response = client.get('/trap/random/')
    assert response._status_code == 200


def test_outgoing(client):
    response = client.get('/trap/outgoing/')
    assert response._status_code == 200


def test_login(client):
    response = client.get('/trap/login/')
    assert response._status_code == 200


def test_cookies(client):
    response = client.get('/trap/cookies/')
    assert response._status_code == 200


def test_recaptcha_without_key(client):
    response = client.get('/trap/recaptcha/')
    assert response._status_code == 500


def test_depth(client):
    response = client.get('/trap/depth/')
    assert response._status_code == 200


def test_calendar(client):
    response = client.get('/trap/calendar/')
    assert response._status_code == 200


def test_registration(client):
    response = client.get('/trap/registration/')
    assert response._status_code == 200
