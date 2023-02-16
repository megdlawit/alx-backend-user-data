#!/usr/bin/env python3
""" module for a flask app
"""
from cgitb import reset
from crypt import methods
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """ basic Flask app returning message """
    return jsonify(message='Bienvenue')


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ method to register user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ method to check if email and pass are valid
        and generate session id for login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    resp = make_response()
    if AUTH.valid_login(email=email, password=password):
        sess_id = AUTH.create_session(email=email)
        resp = make_response(jsonify({"email": email,
                                      "message": "logged in"}))
        resp.set_cookie("session_id", sess_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ function to destroy session of logged in user
    """
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if not session_id or not usr:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect('/')


@app.route('/profile', strict_slashes=False)
def profile():
    """ function that responds to the GET /profile route.
    """
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if not session_id or not usr:
        abort(403)
    return jsonify({"email": usr.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ function to respond to the
        POST /reset_password route
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email,
                        "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ function to update user password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    newpass = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, newpass)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
