# -*- coding: utf-8 -*-

import datetime
import time
import feedparser

from web.util.db import db

class Feed(db.Document):
    title               = db.StringField(required=True, default="No title")
    link                = db.StringField()
    content             = db.StringField()
    summary             = db.StringField()
    create_date         = db.DateTimeField() # this is item publish date

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

    @classmethod
    def is_saved(cls, title=None, date=None):
        return cls.objects(title=title, create_date=date).first() is not None

    def to_dict(self, user=None):
        d = {
                "id":str(self.id),
                "title":self.title,
                "link":self.link,
                "content":self.content,
                "summary":self.summary,
                "createDate":self.create_date,
                "feedsiteid":str(self.feedsite.id),
                "author":self.feedsite.title
        }

        if user is not None:
            d["isStared"] = user.has_stared_feed(feed=self)
        return d


class FeedSite(db.Document):
    feed_url            = db.StringField(required=True) # the user input
    site_link           = db.StringField() # we calculate it
    title               = db.StringField()
    fav_icon            = db.StringField() # url->need site_link
    subtitle            = db.StringField() # a summary for site
    create_time         = db.DateTimeField(default=datetime.datetime.now)

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
            pass # send a job to rabbitMQ?
        else:
            site._parse()

        return site.save() # need to try-catch?

    @classmethod
    def get_from_feed_url(cls,feed_url):
        return cls.objects(feed_url=feed_url).first()
        
    def get_last_feed(self,skip=0):
        return Feed.objects(feedsite=self).skip(skip).first()

    @classmethod
    def refresh(cls):
        feed_sites = cls.objects().all()
        for feedsite in feed_sites:
            d = feedparser.parse(feedsite.feed_url)
            if "rss" in d.version:
                feedsite._parse_rss(d)
            else:
                feedsite._parse_atom(d)


    def _refresh_rss(self):
        pass

    def _refresh_atom(self):
        pass

    # only use when the site get feed_url
    # to create feedsite object
    # error handle?
    # TODO
    def _parse(self):
        d = feedparser.parse(self.feed_url)
        if "rss" in d.version:
            self._parse_rss(d)
        else:
            self._parse_atom(d)

    def _parse_rss(self,d):
        self.title          = d.feed.title
        self.subtitle       = d.feed.subtitle
        self.site_link      = d.feed.link
        self.save()
        #to get fav_icon

        #parse the feeditem
        for entry in d.entries:
            create_date         = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            if Feed.is_saved(title=entry.title, date=create_date):
                continue
            feed                = Feed(title=entry.title)
            feed.link           = entry.link
            if "content" in entry:
                feed.content    = entry.content[0].value
            else:
                feed.content    = entry.description
            feed.summary        = entry.summary
            feed.feedsite       = self
            feed.create_date    = create_date
            feed.save()

    def _parse_atom(self,d):
        self.title          = d.feed.title
        self.subtitle       = d.feed.subtitle
        self.site_link      = d.feed.link
        self.save()
        #to get fav_icon

        #parse the feeditem
        for entry in d.entries:
            create_date         = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            if Feed.is_saved(title=entry.title, date=create_date):
                continue
            feed                = Feed(title=entry.title)
            feed.link           = entry.link
            feed.content        = entry.content[0].value
            feed.summary        = entry.summary
            feed.feedsite       = self
            feed.create_date    = create_date
            feed.save()

    @property
    def feed_item_counter(self):
        return Feed.objects(feedsite=self).count()

    @property
    def domain(self):
        import tldextract
        er = tldextract.extract(self.site_link)
        return er.subdomain + "." + er.domain + "." + er.suffix





















