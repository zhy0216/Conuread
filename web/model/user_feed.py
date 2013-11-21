

from web.util.db import db



# user <-> sites
class Sub(db.Document):
    feedsite            = db.ReferenceField("FeedSite")
    user                = db.ReferenceField("User")
    #counter             = db.IntField(default=0)
    unread_counter      = db.IntField(default=0)
    start_date          = db.DateTimeField()

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['user','feedsite'],'unique': True},
        ]
    }

    @classmethod
    def get_feedsite_by_user(cls, user):
        return [sub.feedsite for sub in cls.objects(user=user)]

    @classmethod
    def get_sub_by_user_feedsite(cls,user=None,feedsite=None):
        return cls.objects(user=user,feedsite=feedsite).first()

    @classmethod
    def get_unread_counter_by_user_feedsite(cls,user=None,feedsite=None):
        sub = cls.objects(user=user,feedsite=feedsite).only("unread_counter").first()
        if sub:
            return sub.unread_counter
        return 0

    @classmethod
    def add_sub(cls,user,feedsite):
        from feed import Feed
        sub = cls(user=user,feedsite=feedsite)
        sub.user = user
        sub.feedsite = feedsite
        temp = feedsite.feed_item_counter
        sub.unread_counter = temp if temp <=15 else 15
        sub.start_date = feedsite.get_last_feed(skip=sub.unread_counter-1).create_date
        sub.save()

        feeds = Feed.get_feed_items_by_site(site=feedsite,
                                              limit=temp)
        for feed in feeds:
            ReadFeed.add(feed,user)

        return sub

    @classmethod
    def exist_sub(cls,user=None,feedsite=None):
        return cls.objects(user=user,feedsite=feedsite).first() is not None




# all user sub subscript is in uncategoried folder

#user <-> feeds, means use start a feed;
#it is possible that user can star a feed but have not read it
class StarFeed(db.Document):
    pass


#user <-> feeds, means user has read the feed
class ReadFeed(db.Document):
    feed            = db.ReferenceField("Feed")
    user            = db.ReferenceField("User")
    unread          = db.BooleanField(default=True)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['feed','user'], 'unique': True},
        ]
    }

    @classmethod
    def add(cls,feed,user):
        return cls(feed=feed,user=user).save()

    def safe_save(self):
        self.save()

    @classmethod
    def get_readfeed_by_feed_and_user(cls,feed=None, user=None):
        return ReadFeed.objects(feed=feed,user=user).first()

    @classmethod
    def get_rencent_unread_feeds_by_user(cls, user=None):
        return [rf.feed for rf in cls.objects(user=user, unread=True)\
                                     .only("feed").order_by("-feed__create_date")]


