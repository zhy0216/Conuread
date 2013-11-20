# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask.ext.script import Manager

from web.config import config
from web.application import app

manager = Manager(app)

@manager.command
def clean_db():
    from pymongo import MongoClient
    conn = MongoClient(config.MONGODB_HOST, config.MONGODB_PORT)
    conn.drop_database(config.MONGODB_DB)
    conn.close()

@manager.command
def make_guest():
    from conure.model import BasicUser,UserInfo
    b_user = BasicUser(email="guest",
                          password="guest",
                          info=UserInfo())
    b_user.info.nickname = "Guest"
    b_user.save()
    
@manager.command
def test_init():
    clean_db()
    make_guest()

if __name__ == "__main__":
    manager.run()









