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


def test_blog(client):
    rv = client.get('/modes/blog/')
    assert rv._status_code == 200


def test_forum(client):
    rv = client.get('/modes/forum/')
    assert rv._status_code == 200


def test_newsfeed(client):
    rv = client.get('/modes/newsfeed/')
    assert rv._status_code == 200


def test_forms(client):
    rv = client.get('/modes/forms/')
    assert rv._status_code == 200


def test_catalog(client):
    rv = client.get('/modes/catalog/')
    assert rv._status_code == 200


def test_errors(client):
    rv = client.get('/trap/errors/')
    assert rv._status_code == 200


def test_random(client):
    rv = client.get('/trap/random/')
    assert rv._status_code == 200


def test_outgoing(client):
    rv = client.get('/trap/outgoing/')
    assert rv._status_code == 200


def test_login(client):
    rv = client.get('/trap/login/')
    assert rv._status_code == 200


def test_cookies(client):
    rv = client.get('/trap/cookies/')
    assert rv._status_code == 200


def test_recaptcha_without_key(client):
    rv = client.get('/trap/recaptcha/')
    assert rv._status_code == 500


def test_depth(client):
    rv = client.get('/trap/depth/')
    assert rv._status_code == 200


def test_calendar(client):
    rv = client.get('/trap/calendar/')
    assert rv._status_code == 200


def test_registration(client):
    rv = client.get('/trap/registration/')
    assert rv._status_code == 200
