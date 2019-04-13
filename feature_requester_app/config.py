from feature_requester_app import get_env_var


class BaseConfiguration(object):

    # Recommended by SQLAlchemy to reduce overhead in database operations
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = get_env_var(
        'DATABASE_URL',
        default="sqlite:///:memory:"
    )
    SECRET_KEY = get_env_var('SECRET_KEY', default='my_secret_key')


class DebugConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfiguration(DebugConfiguration):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfiguration(BaseConfiguration):
    DEBUG = False
