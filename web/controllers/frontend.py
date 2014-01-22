# -*- coding: utf-8 -*-

import hashlib

from flask import (render_template, g, session,
                   jsonify, request,redirect)

from web.app import app
from web.model import (User, UserInfo,UserSetting,BasicUser,
                        AdvancedUser,FeedSite, Feed, Sub)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    password = hashlib.sha512(password).hexdigest()

    user = User.validate_user(username=username, 
                              password=password)
    if user is None:
        return jsonify(dict(rcode=404))

    g.user = user
    session["user"] = g.user.to_dict()

    return redirect("/")

@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form.get("username")
    password = request.form.get("password")

    password = hashlib.sha512(password).hexdigest()

    user = User.validate_user(username=username, 
                              password=password)
    if user is None:
        return jsonify(dict(rcode==404))

    g.user = user
    session["user"] = g.user.to_dict()

    return jsonify(rcode=200)

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    nickname = request.form.get("nickname")

    password = hashlib.sha512(password).hexdigest()

    
    user = BasicUser.register(username=username, 
                              password=password, 
                              nickname=nickname)
    g.user = user
    session["user"] = g.user.to_dict()


    return jsonify(rcode=200,data=render_template("plugin/user.html"))



@app.route("/logout")
def logout():
    session.pop("user")
    g.user.activate = False
    return jsonify(dict(rcode=200, data=render_template("plugin/user.html")))
