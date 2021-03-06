

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
    def get_unread_counter_by_user(cls,user=None):
        subs = cls.objects(user=user).only("unread_counter")
        if len(subs):
            return sum(map(lambda x:x.unread_counter, subs))
        return 0

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
        
        # sub.start_date = feedsite.get_last_feed(skip=sub.unread_counter-1).create_date
        

        feeds = Feed.get_feed_items_by_site(site=feedsite,
                                              limit=temp)
        for feed in feeds[:500]:
            if not user.has_feed(feed=feed):
                ReadFeed.add(feed=feed,user=user,feedsite=feedsite)
                sub.unread_counter += 1
        sub.save()
        return sub


    @classmethod
    def exist_sub(cls,user=None,feedsite=None):
        return cls.objects(user=user,feedsite=feedsite).first() is not None


    @classmethod
    def refresh_sub(cls, feedsite=None, new_feeds=None):
        subs = cls.objects(feedsite=feedsite)
        for sub in subs:
            sub.unread_counter += len(new_feeds)
            sub.save()

            for feed in new_feeds:
                ReadFeed.add(feed=feed,user=sub.user,feedsite=feedsite)


# all user sub subscript is in uncategoried folder

#user <-> feeds, means use start a feed;
#it is possible that user can star a feed but have not read it
class StarFeed(db.Document):
    feed            = db.ReferenceField("Feed")
    user            = db.ReferenceField("User")
    # add feed create date field?

    @classmethod
    def user_star_feed(cls, user=None, feed=None):
        sf = cls._get_star_feed_by_user_feed(user=user, feed=feed)
        if sf is None:
            sf = cls(feed=feed, user=user).save()
        return sf

    @classmethod
    def user_unstar_feed(cls, user=None, feed=None):
        sf = cls._get_star_feed_by_user_feed(user=user, feed=feed)
        if sf:
            sf.delete()

    @classmethod
    def is_user_star_feed(cls, user=None, feed=None):
        return cls._get_star_feed_by_user_feed(user=user, feed=feed) is not None

    @classmethod
    def _get_star_feed_by_user_feed(cls, user=None, feed=None):
        return cls.objects(user=user, feed=feed).first()

    @classmethod
    def get_feed_by_user(cls, user=None, limit=15, page=1):
        start = limit * page - limit
        end = limit * page
        return sorted([sf.feed for sf in cls.objects(user=user)], 
                       key=lambda x:x.create_date, reverse=True)[start:end]

    @classmethod
    def get_all_unread_feed_by_user(cls, user=None):
        feeds = [x.feed for x in cls.objects(user=user)]
        return filter(lambda x: user.has_read(feed=x),feeds)


#user <-> feeds, means user has read the feed
class ReadFeed(db.Document):
    feed            = db.ReferenceField("Feed")
    feedsite        = db.ReferenceField("FeedSite")
    user            = db.ReferenceField("User")
    unread          = db.BooleanField(default=True)
    # add feed create date field?

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['feed','user'], 'unique': True},
        ]
    }

    @classmethod
    def add(cls,feed=None,user=None,feedsite=None):
        return cls(feed=feed,user=user,feedsite=feedsite).save()

    def safe_save(self):
        self.save()

    @classmethod
    def get_readfeed_by_feed_and_user(cls,feed=None, user=None):
        return ReadFeed.objects(feed=feed,user=user).first()

    @classmethod
    def get_rencent_unread_feeds_by_user(cls, user=None):
        return [rf.feed for rf in cls.objects(user=user, unread=True)\
                                     .only("feed").order_by("-feed__create_date")]

    @classmethod
    def get_rencent_unread_feeds_by_user_feedsite(cls, user=None, feedsite=None, limit=15, page=1):
        start = limit * page - limit
        end = limit * page
        return [rf.feed for rf in cls.objects(user=user, unread=True, feedsite=feedsite)\
                                     .only("feed").order_by("-feed__create_date")][start:end]

