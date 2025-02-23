"""
Handles session management using JWT.
"""

from flask_jwt_extended import create_access_token

REVOKED_TOKENS_FILE = "data/revoked_tokens"

def generate_session_token(username):
    return create_access_token(identity=username)

def revoke_session_token(token):
    with open(REVOKED_TOKENS_FILE, 'a') as f:
        f.write(f"{token}\n")

def verify_session_token(token):
    try:
        with open(REVOKED_TOKENS_FILE, 'r') as f:
            for line in f:
                if line.strip() == token:
                    return False
        return True
    except FileNotFoundError:
        return True