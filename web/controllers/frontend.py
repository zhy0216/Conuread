# -*- coding: utf-8 -*-

from flask import render_template, g, session

from web.app import app
from web.model import FeedSite

@app.route('/')
@app.route('/feedsite/<feedsiteid>')
def read_site(feedsiteid=0):
    sites = FeedSite.objects()
    user = g.user
    if feedsiteid == 0:
        feeds = user.get_rencent_unread_feeds()
    else:
        pass

    return render_template("main.html", 
                            sites=sites,
                            feeds=feeds)





