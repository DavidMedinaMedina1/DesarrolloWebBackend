from crypt import methods
from datetime import datetime
from flask import Flask, render_template, request, session
import datetime
# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"
#############################################################

@app.route('/')
def home():
    email = None
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data = email)
    else:
        return render_template('login.html', data = email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "GET"):
        return render_template("Login.html", data="email")
    else:
        email = None
        email = request.form["email"]
        password = request.form["password"]
        return render_template("index.html", data=email)

