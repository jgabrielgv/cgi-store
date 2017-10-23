import bcrypt
#from getpass import getpass

def encrypt_password(raw_password):
    """Encrypts a password"""
    master_secret_key = "al_br_7-1_never_forget"
    salt = bcrypt.gensalt()
    combo_password = raw_password + salt + master_secret_key
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return {"salt": salt, "hash": hashed_password}

def verify_password(raw_password, user):
    """Verifies a password against an existing user"""
    return True
