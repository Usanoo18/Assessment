import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    
    
    db = sqlite3.connect(".database/user.db")
    db.row_factory = sqlite3.Row
    
    return db

def GetReview():
    
    
    db = GetDB()
    reviews = db.execute("SELECT * FROM Reviews").fetchall()
    db.close()
    return reviews


def CheckLogin(username, password):

    db = GetDB()

    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()

    if user is not None:
        if check_password_hash(user['password'], password):
            return user
        
    return None

def RegisterUser(username, password):
    if username is None or password is None:
        return False
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit

    return True