"""
Handles user registration and authentication using bcrypt to hash passwords.
WARNING: Currently stores users in a linux passwd style file in the form <user>:<hashed-password>
        I suggest coming up with a more secure option in the future.
"""

import bcrypt
PASSWD_FILE = "data/passwd"

def register_user(username, passwd):
    passwd_bytes = passwd.encode('utf-8')
    hashed_passwd = bcrypt.hashpw(passwd_bytes, bcrypt.gensalt())

    # Check that the user doesn't already exist.
    with open(PASSWD_FILE, 'r') as f:
        for line in f:
            if line.startswith(username + ":"):
                return False

    # If it doesn't append the new user to the passwd file.
    with open(PASSWD_FILE, 'a') as f:
        f.write(f"{username}:{hashed_passwd.decode('utf-8')}\n")
        return True

def authenticate_user(username, passwd):
    passwd_bytes = passwd.encode('utf-8')
    with open(PASSWD_FILE, 'r') as f:
        for line in f:
            # Check that the user exists
            if line.startswith(username + ":"):
                # If it does then check the password return True for a match and False otherwise.
                hashed_passwd = line.split(":")[1].strip().encode('utf-8')
                return bcrypt.checkpw(passwd_bytes, hashed_passwd)
    # Otherwise return False because the user was not found.
    return False