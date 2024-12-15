from flask import Flask, redirect, render_template, request, session  # Import necessary modules from Flask
import db  # Import the db module to interact with the database

app = Flask(__name__)  # Initialize the Flask application
app.secret_key = "goku"  

# Route for the homepage (index)
@app.route("/")
def index():
    # Get review data from the database by calling the GetReview function
    reviewData = db.GetReview()
    return render_template("index.html", FetchedReview=reviewData)


# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def Login():
    # If the user is already logged in (session exists), redirect to the homepage
    if 'user.id' in session:
        return redirect("/")
    
    if request.method == "POST":
        # Get the username and password from the submitted form
        username = request.form['username']
        password = request.form['password']

        # Check the login credentials in the database
        user = db.CheckLogin(username, password)
        
        # If login is successful
        if user:
            # Store user info in the session for later use (i.e., keeping the user logged in)
            session['id'] = user['id']
            session['username'] = username
            # Redirect the user to the homepage
            return redirect("/")
    
    # If the request is GET or login fails, render the login.html page
    return render_template("login.html")


# Route to log the user out
@app.route("/logout")
def Logout():
    # Clear the session (logging out the user)
    session.clear()
    
    # Redirect to the homepage after logging out
    return redirect("/")


# Route for the registration page
@app.route("/register", methods=["GET", "POST"])
def Register():
    # If the user is already logged in, redirect to the homepage
    if 'user.id' in session:
        return redirect("/")
    
    if request.method == "POST":
        # Get the username and password from the submitted form
        username = request.form['username']
        password = request.form['password']

        # Register the new user in the database
        if db.RegisterUser(username, password):
            # If registration is successful, redirect to the homepage
            return redirect("/")
    
    # If the request is GET or registration fails, render the register.html page
    return render_template("register.html")


# Route to add a review 
@app.route("/add", methods=["GET", "POST"])
def Add():
    # If the user is not logged in, redirect to the homepage 
    if session.get('username') == None:
        return redirect("/")
    
    if request.method == "POST":
        # Get the user ID from the session (who is submitting the review)
        user_id = session['id']
        
        # Get the form data (review details)
        date = request.form['date']
        type = request.form['type']
        name = request.form['name']
        rating = int(request.form['rating'])
        review = request.form['review']
        
        # Add the review to the database
        success = db.AddReview(user_id, date, type, rating, review, name)
        
        # If the review is successfully added, redirect to the homepage
        if success:
            return redirect("/")
        else:
            # If adding the review fails (due to missing data), stay on the "add review" page
            return redirect("/add")
    
    # Render the add.html page
    return render_template("add.html")


# Run the Flask app on port 5000 with debugging enabled
app.run(debug=True, port=5000)
