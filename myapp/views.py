# -*- coding: utf8 -*-

from flask import render_template

from myapp.app import app

# An absolute import gives us the Doctor, Preference, Medicine model
#from myapp.models import Doctor, Preference, Medicine

@app.route('/')
def use_app():
    """Use our amazing app."""
    # [...]
    #return 'Hello world!'
    return render_template('index.html', title="Hello, world")

