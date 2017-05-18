# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash

UPLOAD_FOLDER = '/var/www/blog/blog/static/images'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER