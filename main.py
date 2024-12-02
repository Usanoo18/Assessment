from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'goku'

@app.route("/")
def home():
    return "This is the home page"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
