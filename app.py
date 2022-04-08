from crypt import methods
#1.-

from flask import Flask, render_template, request, session, redirect, url_for
import datetime
# FlASK
#############################################################
app = Flask(__name__)
#2.-
app.permanent_session_lifetime = datetime.timedelta(days=1)
#3.-
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
    email = None
    if "email" in session:
        return render_template('index.html', data = session["email"])
      #  return redirect(url_for("home"))

    else:    
        if (request.method == "GET"):
            return render_template("Login.html", data="email")
        else:
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email
            return render_template("index.html", data=email)

