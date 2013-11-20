# coding:utf8

import os

from flask.ext.mongoengine import MongoEngine

from web.config import conf

def get_db(database=None):
    if not database:
        database = conf.MONGODB_DB
    if os.environ.get("UNITTEST_MODE"):
        database = conf.MONGODB_DB_UNITTEST
    mongo = MongoEngine()
    mongo.connect(
        database,
        host=conf.MONGODB_HOST,
        port=conf.MONGODB_PORT,
        username=conf.MONGODB_USER,
        password=conf.MONGODB_PASSWD
    )
    return mongo

db = get_db()