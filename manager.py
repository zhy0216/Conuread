# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask.ext.script import Manager

from web.config import conf
from web.app import app

manager = Manager(app)



@manager.command
def refresh_site():
    pass

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

@manager.command
def test_add():
    from web.model.feed import Feed,FeedSite
    from web.model.user import BasicUser
    test_url0 = 'http://feed.williamlong.info/'
    test_url1 = "http://solidot.org.feedsportal.com/c/33236/f/556826/index.rss"
    site0 = FeedSite.add_from_feed_url(test_url0)
    site1 = FeedSite.add_from_feed_url(test_url1)
    b_user = BasicUser.get_user_by_nickname("Guest")
    b_user.sub_feedsite(site0)
    b_user.sub_feedsite(site1)


if __name__ == "__main__":
    manager.run()









