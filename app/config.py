import os
# import redis


class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or "mine-my-precious"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "katDB.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SESSION_PERMANENT = False
    # SESSION_TYPE = "redis"
    # SESSION_REDIS = redis.from_url('redis://localhost:6379')