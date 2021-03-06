# -*- coding: utf-8 *-*

import string,random
import hashlib
import datetime

from faker import Faker

from web.util.db import db
from .feed import FeedSite,Feed

class UserInfo(db.EmbeddedDocument):
    nickname    = db.StringField()

class UserSetting(db.EmbeddedDocument):
    unread_only = db.BooleanField(default=True)
    theme       = db.StringField(default="google")

class User(db.Document):
    username        = db.StringField()
    password        = db.StringField()
    activate        = db.BooleanField(default=False)
    info            = db.EmbeddedDocumentField("UserInfo")
    setting         = db.EmbeddedDocumentField("UserSetting")
    type            = "user"

    meta = {
        'allow_inheritance': True,
        'index_types': False,
        'indexes': [
        ]
    }

    @classmethod
    def validate_user(cls, username=None, password=None):
        return cls.objects(username=username,password=password).first()

    @classmethod
    def gen_user(cls):
        return cls(info=UserInfo(), setting=UserSetting()).save()

    @classmethod
    def get_user_by_id(cls,id):
        return cls.objects(id=id).first()

    @classmethod
    def get_user_by_nickname(cls,nickname):
        return cls.objects(info__nickname=nickname).first()

    def is_activate(self):
        return self.activate

    def activate_me(self):
        self.activate = True
        return self.save()

    def get_rencent_unread_feeds(self):
        from user_feed import ReadFeed

        return ReadFeed.get_rencent_unread_feeds_by_user(user=self)

    def get_unread_feeds_on_feedsite(self, feedsite=None, limit=15, page=1):
        from user_feed import ReadFeed
        return ReadFeed.get_rencent_unread_feeds_by_user_feedsite(user=self,
                                                                  feedsite=feedsite,
                                                                  limit=limit,
                                                                  page=page)

    def get_feedsite(self):
        from user_feed import Sub
        return Sub.get_feedsite_by_user(user=self)

    #
    def has_feedsite(self,feedsite):
        from user_feed import Sub
        return Sub.exist_sub(self,feedsite)

    def read_feed(self,feed):
        from user_feed import ReadFeed,Sub
        rf  = ReadFeed.get_readfeed_by_feed_and_user(feed=feed,
                                        user=self)
        if rf is None:
            return 

        if rf.unread:
            sub  = Sub.get_sub_by_user_feedsite(user=self,
                                                  feedsite=feed.feedsite)
            sub.unread_counter -=1
            sub.save()
        rf.unread = False
        rf.safe_save()


    def unread_feed(self,feed):
        pass

    def has_read(self,feed=None):
        from user_feed import ReadFeed
        rf  = ReadFeed.get_readfeed_by_feed_and_user(feed=feed,user=self)
        return not rf.unread

    def has_feed(self, feed=None):
        from user_feed import ReadFeed
        rf  = ReadFeed.get_readfeed_by_feed_and_user(feed=feed,user=self)
        return rf is not None

    def has_stared_feed(self, feed=None):
        from .user_feed import StarFeed
        return StarFeed.is_user_star_feed(user=self, feed=feed)

    def star_feed(self, feed):
        from .user_feed import StarFeed
        StarFeed.user_star_feed(user=self, feed=feed)

    def unstar_feed(self, feed):
        from .user_feed import StarFeed
        StarFeed.user_unstar_feed(user=self, feed=feed)

    def get_star_feeds(self):
        from .user_feed import StarFeed
        return StarFeed.get_feed_by_user(user=self)

    def sub_feedsite(self, feedsite=None):
        from user_feed import Sub
        from feed import FeedSite

        if self.has_feedsite(feedsite):
            return None

        Sub.add_sub(self,feedsite)
        return feedsite

    def unsub_feedsite(self, feedsite=None):
        from user_feed import Sub, ReadFeed
        from feed import FeedSite

        if self.has_feedsite(feedsite):
            Sub.objects(user=self,feedsite=feedsite).delete()
            # ReadFeed.objects(user=self, feedsite=feedsite).delete()
            return True

    def add_feedsite(self,feed_url=None):
        from user_feed import Sub
        from feed import FeedSite

        fs = FeedSite.get_from_feed_url(feed_url)
        if self.has_feedsite(fs):
            return None
        fs  = FeedSite.add_from_feed_url(feed_url)
        Sub.add_sub(self,fs)
        return fs

    def get_unread_counter(self):
        from user_feed import Sub
        return Sub.get_unread_counter_by_user(user=self)

    def get_unread_counter_on_feedsite(self,feedsite):
        from user_feed import Sub
        counter  = Sub.get_unread_counter_by_user_feedsite(user=self,
                                                            feedsite=feedsite)
        return counter

    def to_dict(self):
        return {"id":str(self.id),
                "nickname":self.info.nickname,
                "type":self.type
        }

    @property
    def nickname(self):
        return self.info.nickname



class BasicUser(User):
    type        = "basic"


    @classmethod
    def register(cls, username=None,
                 nickname=None, password=None):
        from flask import g
        g.user.username = username
        g.user.info.nickname = nickname
        g.user.password = password
        g.user.activate = True

        return g.user.save()

    def upgrade(self):
        pass

    def subscribe(self,site):
        pass

    @classmethod
    def get_guest(cls):
        return cls.objects(username="guest").first()

class AdvancedUser(User):
    pass


