# -*- coding: utf-8 -*-

from flask import render_template

from web.app import app

@app.route('/')
def main():
    return render_template("main.html")