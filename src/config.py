class Config:
    SECRET_KEY = 'Cafecita123'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Cafecita123'
    MYSQL_DB = 'Pachamama'
    ENV = 'development'

config = {
    'development': DevelopmentConfig,
    'default': Config
}
