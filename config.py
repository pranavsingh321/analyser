class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@host:port/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@localhost:port/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@testhost:port/dbname'
    TESTING = True


class ProductionConfig(BaseConfig):
    # TODO: set the db url and the other parameters for the ProductionConfig
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@productionhost:port/dbname'


# Collects all the available configurations in a dictionary
configs = {'dev': DevelopmentConfig,
           'test': TestingConfig,
           'prod': ProductionConfig,
           'default': ProductionConfig}
