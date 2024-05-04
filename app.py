import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
db = SQL("sqlite:///habit.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not (email := request.form.get("email")):
            return apology("Please enter E-mail")
        if not request.form.get("password"):
            return apology("Please enter a password")
        
        rows = db.execute(
            "SELECT email, hash FROM users WHERE email = ?", email
            )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        
        session["user_id"] = rows[0]["id"]
        
        return redirect("/")
    
    else:
        return render_template("login.html")
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



