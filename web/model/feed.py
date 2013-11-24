# -*- coding: utf-8 -*-

import datetime

import feedparser

from web.util.db import db

class Feed(db.Document):
    title               = db.StringField(required=True, default="No title")
    link                = db.StringField()
    content             = db.StringField()
    summary             = db.StringField()
    create_date         = db.DateTimeField(default=datetime.datetime.now) #

    feedsite            = db.ReferenceField("FeedSite")

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'ordering': ['-create_date']
    }
    
    @classmethod
    def get_feed_by_id(cls,feedid):
        return cls.objects(id=feedid).first()

    def is_newer_than(self,tdate):
        pass

    @classmethod
    def get_feed_items_by_site(cls,site,limit=15,offset=0):
        start       = offset*limit
        end         = offset*limit + limit
        return cls.objects(feedsite=site)[start:end]

    def to_dict(self):
        return {
                "id":str(self.id),
                "title":self.title,
                "link":self.link,
                "content":self.content,
                "summary":self.summary,
                "createDate":self.create_date,
                "feedsiteid":str(self.feedsite.id),
        }

class FeedSite(db.Document):
    feed_url            = db.StringField(required=True) # the user input
    site_link           = db.StringField() # we calculate it
    title               = db.StringField()
    fav_icon            = db.StringField() # url->need site_link
    last_pub_time       = db.DateTimeField() #the last time the web site change rss

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['feed_url'], 'unique': True},
        ]
    }



    @classmethod
    def get_feeds_by_id(cls, feedsiteid, limit=15, page=1):
        start = limit * page - limit
        end = limit * page
        return Feed.objects(feedsite=feedsiteid).order_by("-create_date")[start:end]

    @classmethod
    def get_unread_feeds_by_id(cls, feedsiteid, limit=15, page=1):
        start = limit * page - limit
        end = limit * page
        pass

    @classmethod
    def add_from_feed_url(cls,feed_url):
        site    = cls.get_from_feed_url(feed_url) or cls(feed_url=feed_url)
        if site.id:
            site.refresh()
        else:
            site._parse()

        return site.save() # need to try-catch?

    @classmethod
    def get_from_feed_url(cls,feed_url):
        return cls.objects(feed_url=feed_url).first()
        
    def get_last_feed(self,skip=0):
        return Feed.objects(feedsite=self).skip(skip).first()

    def refresh(self):
        print "refresh"

    # only use when the site get feed_url
    # to create feedsite object
    # error handle?
    # TODO
    def _parse(self):
        d = feedparser.parse(self.feed_url)
        self.title          = d.feed.title
        self.site_link      = d.feed.link
        self.save()
        #to get fav_icon

        #parse the feeditem
        for entry in d.entries:
            feed                = Feed(title=entry.title)
            feed.link           = entry.link
            feed.content        = entry.description
            feed.summary        = entry.summary
            feed.feedsite       = self
            feed.save()

    @property
    def feed_item_counter(self):
        return Feed.objects(feedsite=self).count()

    @property
    def domain(self):
        import tldextract
        er = tldextract.extract(self.site_link)
        return er.subdomain + "." + er.domain + "." + er.suffix





















