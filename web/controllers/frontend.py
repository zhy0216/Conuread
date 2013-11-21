# -*- coding: utf-8 -*-

from flask import (render_template, g, session,
                   jsonify, request)

from web.app import app
from web.model import FeedSite

@app.route('/')
@app.route('/feedsite/<feedsiteid>')
def read_site(feedsiteid=0):
    sites = FeedSite.objects()
    user = g.user
    if feedsiteid == 0:
        feeds = [feed.to_dict() for feed in user.get_rencent_unread_feeds()]
    else:
        pass

    return render_template("main.html", 
                            sites=sites,
                            feeds=feeds)


@app.route("/api/feedsite/<feedsiteid>", methods=["GET","POST"])
def feeds(feedsiteid=None):
    if feedsiteid is None:
        return jsonify(dict(rcode=404))

    feeds = [feed.to_dict() for feed in FeedSite.get_feeds_by_id(feedsiteid)]
    return jsonify(dict(rcode=200, feeds=feeds))
