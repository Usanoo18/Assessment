from flask import Flask, render_template, request
import db

app = Flask(__name__)
app.secret_key = 'goku'

@app.route("/")
def Home():
    return render_template("templates/index.html")


app.run(debug=True, port=5000)
