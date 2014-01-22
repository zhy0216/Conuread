# -*- coding: utf-8 -*-

import hashlib

from flask import (render_template, g, session,
                   jsonify, request,redirect)

from web.app import app
from web.model import (User, UserInfo,UserSetting,BasicUser,
                        AdvancedUser,FeedSite, Feed, Sub)





@app.route("/api/feed/<feedid>/read",methods=["POST"])
def read_feed(feedid):
    feed = Feed.get_feed_by_id(feedid)
    g.user.read_feed(feed)
    return jsonify(rcode=200)


@app.route("/api/feed/<feedid>/unread",methods=["POST"])
def unread_feed(feedid):
    feed = Feed.get_feed_by_id(feedid)
    g.user.unread_feed(feed)
    return jsonify(rcode=200)

@app.route("/api/feed/<feedid>/star",methods=["POST"])
def star_feed(feedid):
    feed = Feed.get_feed_by_id(feedid)
    g.user.star_feed(feed)
    return jsonify(rcode=200)


@app.route("/api/feed/<feedid>/unstar",methods=["POST"])
def unstar_feed(feedid):
    feed = Feed.get_feed_by_id(feedid)
    g.user.unstar_feed(feed)
    return jsonify(rcode=200)


