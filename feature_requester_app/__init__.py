import os

from flask import Flask
from dotenv import load_dotenv

# Build paths inside project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_env_var(name, default=None):
    u"""
    Get the environment variables.
    This function tries to get var_name from environment,
    and raises ImproperlyConfigured error if it doesn't find it.
    """
    try:
        return os.environ[name]
    except KeyError:
        if default:
            return default
        raise ImportError(
            'Set the {0} environment variable'.format(name)
        )


def read_env():
    u"""
    Read variables from '.env'.
    Define path for '.env' and load the file.
    """
    dotenv_path = os.path.join(BASE_DIR, '.env')
    try:
        load_dotenv(dotenv_path)
    except IOError:
        raise
        pass


# Call method defined above to load environment variables.
read_env()

app = Flask(__name__)
env = get_env_var(
    'CONFIG_MODULE',
    'feature_requester_app.config.DebugConfiguration')
app.config.from_object(env)
app.config['ENV'] = env

import feature_requester_app.views
