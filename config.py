
# class Config:
#     SECRET_KEY = "MySecKey"
#     SQLALCHEMY_DATABASE_URI="sqlite:///v1.db"
#     SQLALCHEMY_TRACK_MODIFICATION = False

# Using postgres for vercel deployment
import os
import secrets

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://default:lmeuKtvbA9r0@ep-morning-voice-a4ds1ucg.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import redis
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://default:lmeuKtvbA9r0@ep-morning-voice-a4ds1ucg.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(
        host='redis-15695.c232.us-east-1-2.ec2.redns.redis-cloud.com',
        port=15695,
        password='<your_redis_password>'
    )
