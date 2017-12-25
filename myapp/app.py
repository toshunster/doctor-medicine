#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask


app = Flask(__name__)
#app.config.from_pyfile('config.py')

from myapp import views

if __name__ == "__main__":
    app.run()
