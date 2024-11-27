#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python crypt.py 'password'")
        sys.exit(1)
    password = sys.argv[1]
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")
