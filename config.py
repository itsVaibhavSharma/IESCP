
# class Config:
#     SECRET_KEY = "MySecKey"
#     SQLALCHEMY_DATABASE_URI="sqlite:///v1.db"
#     SQLALCHEMY_TRACK_MODIFICATION = False

# Using postgres for vercel deployment
import os
import secrets
import redis

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'your_postgres_url')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(
        host='redis-15695.c232.us-east-1-2.ec2.redns.redis-cloud.com',
        port=15695,
        password='<your_redis_password>'
    )
