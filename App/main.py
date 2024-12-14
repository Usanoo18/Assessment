from flask import Flask, redirect, render_template, request, session
import db

app = Flask(__name__)
app.secret_key = "goku"

@app.route("/")
def index():
    reviewdata = db.GetReview()
    return render_template("index.html", reviews=reviewdata)


@app.route("/login", methods=["GET", "POST"])
def Login():
    if 'user.id' in session:
        return redirect("/")

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = db.CheckLogin(username, password)
        if user:
            session['id'] = user['id']
            session['username'] = username
            return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if 'user.id' in session:
        return redirect("/")

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if db.RegisterUser(username, password):
            return redirect("/")
    return render_template("register.html")


@app.route("/add", methods=["GET","POST"])
def Add():
    if session.get('username') == None:
        return redirect("/")

    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        type = request.form['type']
        name = request.form['name']
        rating = request.form['rating']
        review = request.form['review']
    return render_template("add.html")


app.run(debug=True, port=5000)
