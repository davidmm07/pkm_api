class Config:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pokemon.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False