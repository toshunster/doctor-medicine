#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask
from flask_mongoalchemy import MongoAlchemy

# Configuration.
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Create the little application object.
app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'medicine'

db = MongoAlchemy(app)
#print( dir( db ) )
from myapp import views

if __name__ == "__main__":
    app.run( host='0.0.0.0' )
