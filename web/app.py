import os

import flask as f
from flask import Flask
import flask.ext.assets as fassets

import config.conf as conf

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
def something_before_request():
    pass

import controllers