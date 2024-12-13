from flask import Flask, redirect, render_template, request, session
import db

app = Flask(__name__)
app.secret_key = 'goku'

@app.route("/")
def Home():
    reviewdata = db.GetReview()
    return render_template("index.html", reviews=reviewdata)


@app.route("/login", methods=["GET", "POST"])
def Login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = db.CheckLogin(username, password)
        if user:
            session['id'] = user['id']
            session['username'] = username
            return redirect("/")
    
    return render_template("login.html")

def Logout():
    session.clear()
    return redirect("/")



app.run(debug=True, port=5000)
