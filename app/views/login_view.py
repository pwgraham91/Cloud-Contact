import json
from urllib2 import HTTPError

import flask
from flask import redirect
from flask import request
from flask import session as flask_session
from flask import url_for
from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager
from app.models import User
from app.views.handlers.auth_handler import get_google_auth
from config import Auth, ENVIRONMENT


@login_manager.user_loader
def load_user(user_id):
    session = db.session
    return session.query(User).get(user_id)


@app.route('/dev-login/<int:user_id>')
def dev_login(user_id):
    if ENVIRONMENT == 'dev':
        login_user(db.session.query(User).get(user_id))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))


@app.route('/register', methods=['GET'])
def register_get():
    return flask.render_template('register.html')


@app.route('/login_form', methods=['GET'])
def login_get():
    return flask.render_template('login_form.html')


@app.route('/register', methods=['POST'])
def register_post():
    session = db.session

    form = flask.request.form
    user = User(
        name=form['name'],
        email=form['email'],
        password=generate_password_hash(form['password'])
    )
    session.add(user)
    session.commit()
    login_user(user)
    return redirect(url_for('index'))


@app.route('/login_form', methods=['POST'])
def login_post():
    session = db.session
    form = flask.request.form
    user = session.query(User).filter(
        User.email == form['email']
    ).first()
    if check_password_hash(user.password, form['password']):
        login_user(user)
        return redirect(url_for('index'))
    else:
        return 'wrong password'


@app.route('/gCallback')
def callback():
    current_user = flask.g.user
    session = db.session

    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You are denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=flask_session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url.replace('http://', 'https://'),
            )
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        # todo: cool stuff in here
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(
                    name=user_data['name'] or user_data['email'].split('@')[0].capitalize(),
                    email=email,
                    avatar=user_data['picture']
                )
            user.tokens = json.dumps(token)
            session.add(user)
            session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'
