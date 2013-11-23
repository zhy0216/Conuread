# -*- coding: utf-8 *-*

import string,random
import hashlib
from datetime import datetime as dt

from web.util.db import db
from .feed import FeedSite,Feed

class Validator(object):
    email       = db.StringField(required=True)
    password    = db.StringField(required=True)

    @classmethod
    def is_valid(cls,email,password):
        user = cls.objects(email=email,password=password).first()
        return user is not None

    @classmethod
    def validate_user(cls, email, password):
        return cls.objects(email=email,password=password).first()

class UserInfo(db.EmbeddedDocument):
    nickname    = db.StringField(required=True)

class UserSetting(db.EmbeddedDocument):
    theme       = db.StringField(default="google")

class User(db.Document):
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
    def get_user_by_id(cls,id):
        return cls.objects(id=id).first()

    @classmethod
    def get_user_by_nickname(cls,nickname):
        return cls.objects(info__nickname=nickname).first()

    def get_rencent_unread_feeds(self):
        from user_feed import ReadFeed

        return ReadFeed.get_rencent_unread_feeds_by_user(user=self) 

    def get_feedsite(self):
        from user_feed import Sub
        return Sub.get_feedsite_by_user(user=self)

    #
    def has_feedsite(self,feedsite):
        from user_feed import Sub
        return Sub.exist_sub(self.id,feedsite)

    def read_feed(self,feed):
        from user_feed import ReadFeed,Sub
        rf  = ReadFeed.get_readfeed_by_feed_and_user(feed=feed,
                                        user=self)
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
        rf  = ReadFeed.get_readfeed_by_feed_and_userid(feed=feed,userid=self.id)
        return not rf.unread

    def sub_feedsite(self, feedsite=None):
        from user_feed import Sub
        from feed import FeedSite

        if self.has_feedsite(feedsite):
            return None

        Sub.add_sub(self,feedsite)
        return feedsite

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


    def upgrade(self):
        pass

    def subscribe(self,site):
        pass

class AdvancedUser(User):
    pass


