"""
Handles session management using JWT.
"""

from flask_jwt_extended import create_access_token

def generate_session_token(username):
    return create_access_token(identity=username)