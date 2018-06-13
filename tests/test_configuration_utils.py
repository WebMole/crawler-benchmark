import matplotlib

matplotlib.use('Agg')

import os

import mock as mock

from project.configuration.utils import env_var


def test_env_var_unset():
    assert env_var('UNSET_ENV_VAR') is None


@mock.patch.dict(os.environ, {'FALSE_ENV_VAR': 'False'})
def test_env_var_false():
    assert env_var('FALSE_ENV_VAR') is False


@mock.patch.dict(os.environ, {'TRUE_ENV_VAR': 'True'})
def test_env_var_true():
    assert env_var('TRUE_ENV_VAR') is True


@mock.patch.dict(os.environ, {'FOO': 'bar'})
def test_env_var_str():
    assert env_var('FOO') is 'bar'
