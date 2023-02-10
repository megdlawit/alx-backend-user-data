#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = getenv('AUTH_TYPE')
if auth == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

request_list = ['/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/',
                '/api/v1/auth_session/login/']


@app.before_request
def filter_request() -> None:
    """ Filter requests for authorization
    """
    if auth is None:
        return
    if not auth.require_auth(request.path, request_list):
        return
    if (not auth.authorization_header(request) and
            not auth.session_cookie(request)):
        abort(401)
    request.current_user = auth.current_user(request)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_found(error) -> str:
    """ Unauthorized request handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_found(error) -> str:
    """ Forbidden request handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
