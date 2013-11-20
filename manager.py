# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask.ext.script import Manager

from web.config import conf
from web.app import app

manager = Manager(app)

@manager.command
def clean_db():
    from pymongo import MongoClient
    conn = MongoClient(conf.MONGODB_HOST, conf.MONGODB_PORT)
    conn.drop_database(conf.MONGODB_DB)
    conn.close()

@manager.command
def make_guest():
    from web.model import BasicUser,UserInfo
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









