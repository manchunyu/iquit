import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

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
        if not request.form.get("email"):
            return -1
        if not request.form.get("password"):
            return -1
    
    else:
        return render_template("login.html")
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


