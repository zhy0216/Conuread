# -*- coding: utf-8 -*-

import hashlib

from flask import (render_template, g, session,
                   jsonify, request,redirect, flash)

from web.app import app
from web.model import (User, UserInfo,UserSetting,BasicUser,
                        AdvancedUser,FeedSite, Feed, Sub, ReadFeed)


@app.route("/api/pop-feedsite/sub", methods=["POST"])
def sub_pop_feedsite():
    feedsiteid = request.form.get("feedsiteid")
    feedsite = FeedSite.get_feedsite_by_id(feedsiteid)
    if feedsite == None:
        flash("add %s failed"%feedsite.title)
        return jsonify(dict(rcode=404))

    g.user.sub_feedsite(feedsite)
    flash("add %s sucessfully"%feedsite.title)

    return jsonify(dict(rcode=200))


@app.route("/api/pop-feedsite/<feedsiteid>/", methods=["GET","POST"])
def pop_feeds(feedsiteid=None):
    if feedsiteid is None:
        return jsonify(dict(rcode=404))

    feeds = [feed.to_dict() for feed in Feed.objects(feedsite=feedsiteid).order_by("-create_date")[:15]]
    return jsonify(dict(rcode=200, feeds=feeds))




