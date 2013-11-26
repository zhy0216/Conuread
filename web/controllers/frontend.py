# -*- coding: utf-8 -*-

from flask import (render_template, g, session,
                   jsonify, request)

from web.app import app
from web.model import (User, UserInfo,UserSetting,BasicUser,
                        AdvancedUser,FeedSite, Feed, Sub)

@app.route('/')
@app.route('/feedsite/<feedsiteid>')
def read_site(feedsiteid="all"):
    user = g.user
    sites = user.get_feedsite()
    site_dict = []
    for site in sites:
        d = {}
        d["id"] = str(site.id)
        d["domain"] = site.domain
        d["unreadCount"] = user.get_unread_counter_on_feedsite(site)
        d["title"] = site.title
        site_dict.append(d)


    if feedsiteid == "all":
        feeds = [feed.to_dict() for feed in user.get_rencent_unread_feeds()]
    else:
        pass

    return render_template("main.html", 
                            sites=site_dict,
                            feeds=feeds,
                            feedsiteid=feedsiteid)

@app.route("/become", methods=["POST"])
def become_user():
    username = request.form.get("username")
    password = request.form.get("password")
    nickname = request.form.get("nickname")

    if User.validate_user(username=username, password=password):
        pass

    user = BasicUser.register(username=username, 
                              password=password, 
                              nickname=nickname)


@app.route("/api/feedsite/sub", methods=["POST"])
def sub_site():
    url = request.form.get("url")
    feedsite =  FeedSite.add_from_feed_url(url)
    if feedsite == None:
        return jsonify(dict(rcode=404))
    g.user.sub_feedsite(feedsite)
    site_dict = {}
    site_dict["id"] = str(feedsite.id)
    site_dict["domain"] = feedsite.domain
    site_dict["unreadCount"] = g.user.get_unread_counter_on_feedsite(feedsite)
    site_dict["title"] = feedsite.title

    return jsonify(dict(rcode=200, feedsite=site_dict))


@app.route("/api/feedsite/<feedsiteid>", methods=["GET","POST"])
def feeds(feedsiteid=None):
    if feedsiteid is None:
        return jsonify(dict(rcode=404))

    if feedsiteid == "all":
        feeds = [feed.to_dict() for feed in g.user.get_rencent_unread_feeds()]
    elif feedsiteid == "star":
        feeds = []
    else:
        feeds = [feed.to_dict() for feed in g.user.get_unread_feeds_on_feedsite(feedsiteid)]
    return jsonify(dict(rcode=200, feeds=feeds))

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


