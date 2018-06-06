import os


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.getenv(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val
