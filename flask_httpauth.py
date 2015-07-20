"""
    flask_httpauth
    ==================
    
    This module provides Basic and Digest HTTP authentication for Flask routes.
    
    :copyright: (C) 2014 by Miguel Grinberg.
    :license:   BSD, see LICENSE for more details.
    """

from functools import wraps
from hashlib import md5
from random import Random, SystemRandom
from flask import request, make_response, session


class HTTPAuth(object):
    def __init__(self):
        def default_get_password(username):
            return None
        
        def default_auth_error():
            return "Unauthorized Access"
        
        self.realm = "Authentication Required"
        self.get_password(default_get_password)
        self.error_handler(default_auth_error)
    
    def get_password(self, f):
        self.get_password_callback = f
        return f
    
    def error_handler(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = f(*args, **kwargs)
            if type(res) == str:
                res = make_response(res)
                res.status_code = 401
            if 'WWW-Authenticate' not in res.headers.keys():
                res.headers['WWW-Authenticate'] = self.authenticate_header()
            return res
        self.auth_error_callback = decorated
        return decorated
    
    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("X-TUSO-Application-Token")
            
            # We need to ignore authentication headers for OPTIONS to avoid
            # unwanted interactions with CORS.
            # Chrome and Firefox issue a preflight OPTIONS request to check
            # Access-Control-* headers, and will fail if it returns 401.
            if request.method != 'OPTIONS':
                if token and not self.authenticate(token):
                    return self.auth_error_callback()
            return f(*args, **kwargs)
        return decorated
    
    def username(self):
        if not request.authorization:
            return ""
        return request.authorization.username


class HTTPTokenAuth(HTTPAuth):
    def __init__(self):
        super(HTTPTokenAuth, self).__init__()
        self.hash_password(None)
        self.verify_token(None)
    
    def hash_password(self, f):
        self.hash_password_callback = f
        return f
    
    def verify_token(self, f):
        self.verify_token_callback = f
        return f
    
    def authenticate_header(self):
        return 'Basic realm="{0}"'.format(self.realm)
    
    def authenticate(self, token):
        if not token:
            return False
        
        if self.verify_token_callback:
            return self.verify_token_callback(token)
        
        return False

