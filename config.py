from keys import app_config_key


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql:///myChi"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = app_config_key


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql:///myChi_test"
    TESTING = True
    DEBUG_TB_HOSTS = "dont-show-debug-toolbar"
