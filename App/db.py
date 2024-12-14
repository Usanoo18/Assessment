import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    
    
    db = sqlite3.connect("App/.database/user.db")
    db.row_factory = sqlite3.Row
    
    return db

def GetReview():
    
    
    db = GetDB()
    reviews = db.execute("""SELECT Reviews.date, Reviews.type, Reviews.name, Reviews.rating, Users.username
                         FROM Reviews JOIN Users ON Reviews.user_id = Users.id
                         ORDER BY date DESC""").fetchall()
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

def AddReview(user_id, date, type, rating, review, name):
    if date is None or type is None or rating is None or review is None or name is None:
        return False
    
    db=GetDB()
    db.execute("INSERT INTO Reviews(user_id, type, name, rating, review, date ) VALUES (?, ?, ?, ?, ?, ?)", (user_id, type, name, rating, review, date,))
    db.commit
    return True