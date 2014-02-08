# -*- coding: utf-8 -*-

import hashlib

from flask import (render_template, g, session,
                   jsonify, request,redirect)

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
        feeds = [feed.to_dict(user=g.user) for feed in user.get_rencent_unread_feeds()]
    else:
        pass

    return render_template("main.html", 
                            sites=site_dict,
                            feeds=feeds,
                            feedsiteid=feedsiteid)




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

@app.route("/api/feedsite/<feedsiteid>/unsub", methods=["POST"])
def unsub_site(feedsiteid):
    feedsite  = FeedSite.get_feedsite_by_id(feedsiteid)
    g.user.unsub_feedsite(feedsite)
    return jsonify(dict(rcode=200))


@app.route("/api/feedsite/<feedsiteid>", methods=["GET","POST"])
def feeds(feedsiteid=None):
    if feedsiteid is None:
        return jsonify(dict(rcode=404))

    if feedsiteid == "all":
        feeds = [feed.to_dict(user=g.user) for feed in g.user.get_rencent_unread_feeds()]
    elif feedsiteid == "star":
        feeds = [feed.to_dict(user=g.user) for feed in g.user.get_star_feeds()]
    else:
        feeds = [feed.to_dict() for feed in g.user.get_unread_feeds_on_feedsite(feedsiteid)]
    return jsonify(dict(rcode=200, feeds=feeds))

@app.route("/api/feedsite/<feedsiteid>/mark-all-as-read", methods=["POST"])
def mark_all_as_read(feedsiteid=None):
    if feedsiteid is None:
        return jsonify(dict(rcode=404))



