Flask-HTTPAuth
==============

Simple extension that provides Basic and Digest HTTP authentication for Flask routes.

Basic authentication example
----------------------------

    from flask import Flask, g
    from flask_httpauth import HTTPBasicAuth
    
    app = Flask(__name__)
    auth = HTTPTokenAuth()
    
    users = {
        "john": "hello",
        "susan": "bye"
    }
    
    @verify_token
    def verify_token(token):
        user = User.get_token(verify_token)
        if user
            g.current_user = user
            return True
        return False
    
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, %s!" % g.current_user.username()
        
    if __name__ == '__main__':
        app.run()
        
Fork From: [documentation](http://pythonhosted.org/Flask-HTTPAuth) for more complex examples that involve password hashing and custom verification callbacks.


---------

- [Documentation](http://pythonhosted.org/Flask-HTTPAuth)
- [pypi](https://pypi.python.org/pypi/Flask-HTTPAuth) 

