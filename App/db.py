import sqlite3  # Importing the sqlite3 library to interact with SQLite databases
from werkzeug.security import generate_password_hash, check_password_hash  # Importing functions to hash and check passwords

# Function to get a database connection
def GetDB():
    db = sqlite3.connect("App\.database\loads.db")
    
    db.row_factory = sqlite3.Row

    return db


# Function to get all reviews from the database
def GetReview():
    # Call GetDB to establish a connection to the database
    db = GetDB()
    
    # Execute a SQL query to fetch reviews along with the usernames of users who posted them
    FetchedReview = db.execute("""SELECT Reviews.date, Reviews.type, Reviews.name, Reviews.rating, Reviews.review, Users.username
                                 FROM Reviews JOIN Users ON Reviews.user_id = Users.id
                                 ORDER BY date DESC"""
                                ).fetchall()  # Fetch all results as a list of rows (each row is a dictionary)
    
    # Close the database connection
    db.close()
    
    # Return the fetched reviews
    return FetchedReview


# Function to check if the login credentials (username and password) are correct
def CheckLogin(username, password):
    # Establish a database connection
    db = GetDB()

    # Execute a query to find the user by username
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    
    # If the user exists, check if the password matches the stored hashed password
    if user is not None:
        if check_password_hash(user['password'], password):  # Validate the password hash
            return user  # Return the user data if the password is correct
    
    return None  # Return None if user not found or password does not match


# Function to register a new user
def RegisterUser(username, password):
    if username is None or password is None:
        return False
    
    # Establish a database connection
    db = GetDB()
    
    # Hash the password using Werkzeug's hash function
    hash = generate_password_hash(password)
    
    # Execute a query to insert the new user into the Users table
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    
    # Commit the changes to save the new user
    db.commit()

    return True


# Function to add a new review
def AddReview(user_id, date, type, rating, review, name):
    # Check if any required data is missing
    if date is None or type is None or rating is None or review is None or name is None:
        return False  # Return False if any required field is missing
    
    # Establish a database connection
    db = GetDB()
    
    # Insert the new review into the Reviews table, using the provided data
    db.execute("INSERT INTO Reviews(user_id, type, name, rating, review, date) VALUES (?, ?, ?, ?, ?, ?)",
               (user_id, type, name, rating, review, date,))
    
    # Commit the changes to save the review
    db.commit()

    return True
