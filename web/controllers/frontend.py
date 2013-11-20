# -*- coding: utf-8 -*-

from flask import render_template

from web.app import app
from web.model import FeedSite

@app.route('/')
def main():
    sites = FeedSite.objects()
    return render_template("main.html", sites=sites)