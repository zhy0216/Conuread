import os

from flask import Flask, session, g
import flask.ext.assets as fassets

import config.conf as conf
from web.model import BasicUser,User

app = Flask(__name__)

app.config.from_object("web.config.conf")

assets = fassets.Environment(app)
assets.versions = 'hash:32'
main_js = fassets.Bundle("main_bundle.js",
                        output='dist/main_bundle.%(version)s.js')
assets.register('js_all', main_js)

all_css = fassets.Bundle("style.css",
                         output='dist/main.%(version)s.css')
assets.register('css_all', all_css)

@app.before_request
def check_user_before_request():
    if "user" not in session:
        g.user = BasicUser.gen_user()
        session["user"] = g.user.to_dict()
    else:
        userid = session.get('user')["id"]
        user = User.get_user_by_id(userid)

        # this for when clear db usage
        if user is None:
            user = BasicUser.gen_user()
            session["user"] = user.to_dict()
        g.user = user

@app.context_processor
def inject_user():
    return dict(cur_user=g.user)


import controllers

# from util.filter import timesince
# app.jinja_env.filters['timesince']  = timesince