

from conure.libs.db import db
from .user import UserAccesser



# user <-> sites
class Sub(db.Document,UserAccesser):
    feedsite            = db.ReferenceField("FeedSite")
    #counter             = db.IntField(default=0)
    unread_counter      = db.IntField(default=0)
    start_date          = db.DateTimeField()

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['userid','feedsite'],'unique': True},
        ]
    }

    @classmethod
    def get_sub_by_userid_feedsite(cls,userid=None,feedsite=None):
        return cls.objects(userid=userid,feedsite=feedsite).first()

    @classmethod
    def get_unread_counter_by_userid_feedsite(cls,userid=None,feedsite=None):
        return cls.objects(userid=userid,feedsite=feedsite).only("unread_counter").first().unread_counter

    @classmethod
    def add_sub(cls,userid,feedsite):
        from feed import Feed
        self                    = cls(userid=userid,feedsite=feedsite)
        self.userid             = userid
        self.feedsite           = feedsite
        temp                    = feedsite.feed_item_counter
        self.unread_counter     = temp if temp <=15 else 15
        self.start_date         = feedsite.get_last_feed(skip=self.unread_counter-1).create_date
        self.save()

        feeds                   = Feed.get_feed_items_by_siteid(siteid=feedsite.id,
                                                                limit=temp)
        for feed in feeds:
            ReadFeed.add(feed,userid)

        return self

    @classmethod
    def exist_sub(cls,userid=None,feedsite=None):
        return cls.objects(userid=userid,feedsite=feedsite).first() is not None




# all user sub subscript is in uncategoried folder

#user <-> feeds, means use start a feed;
#it is possible that user can star a feed but have not read it
class StarFeed(db.Document,UserAccesser):
    pass


#user <-> feeds, means user has read the feed
class ReadFeed(db.Document,UserAccesser):
    feed            = db.ReferenceField("Feed")
    unread          = db.BooleanField(default=True)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['feed','userid'], 'unique': True},
        ]
    }

    @classmethod
    def add(cls,feed,userid):
        return cls(feed=feed,userid=userid).save()

    def safe_save(self):
        self.save()

    @classmethod
    def get_readfeed_by_feed_and_userid(cls,feed=None, userid=None):
        return ReadFeed.objects(feed=feed,userid=userid).first()



