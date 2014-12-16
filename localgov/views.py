import os
import jinja2
import json
from flask import Flask, request, redirect, render_template, url_for, session, flash, abort, current_app
from flask_oauthlib.client import OAuth, OAuthException
from localgov import app, oauth

registry = oauth.remote_app(
    'registry',
    consumer_key=app.config['REGISTRY_CONSUMER_KEY'],
    consumer_secret=app.config['REGISTRY_CONSUMER_SECRET'],
    request_token_params={'scope': 'person:view licence:view licence:add'},
    base_url=app.config['REGISTRY_BASE_URL'],
    request_token_url=None,
    access_token_method='POST',
    access_token_url='%s/oauth/token' % app.config['REGISTRY_BASE_URL'],
    authorize_url='%s/oauth/authorize' % app.config['REGISTRY_BASE_URL']
)

#views
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/verify')
def verify():
    return registry.authorize(callback=url_for('verified', _external=True))

@app.route('/verified')
def verified():

    resp = registry.authorized_response()

    if resp is None or isinstance(resp, OAuthException):
        return 'Access denied: reason=%s error=%s' % (
        request.args['error_reason'],
        request.args['error_description']
        )

    session['registry_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))

