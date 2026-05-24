import sqlite3
import hashlib
import pickle
import os

# A02: weak hashing of a password
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# A03: SQL injection via string concatenation
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

# A08: insecure deserialization
def load_session(blob):
    return pickle.loads(blob)

# A03: command injection
def ping(host):
    os.system("ping -c 1 " + host)

# A05: debug mode on in production
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.run(debug=True)
