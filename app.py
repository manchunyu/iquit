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
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def habits():
    if request.method == "POST":
        habit = request.form.get("habit")
        if not habit:
            return apology("Please enter a habit")
        
        starting_streak = 0
        time = datetime.datetime.now()
        db.execute("INSERT INTO habits(users_id, habit, start_time, enter_time, streak) VALUES(?, ?, ?)", 
                   session["user_id"], habit, time, time, starting_streak)

        return redirect("/dashboard")
    
    else:
        common_habits = ["Smoking", "Gambling", "Drinking alcohol", "Drug use", "Poor diet",
                         "Social media scrolling", "Others"]
        return render_template("add.html", common_habits=common_habits)
        
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET","POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not (email := request.form.get("email")):
            return apology("Please enter E-mail")
        if not request.form.get("password"):
            return apology("Please enter a password")
        
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", email
            )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        
        session["user_id"] = rows[0]["id"]
        
        return redirect("/dashboard")
    
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        user_infos = [first_name, last_name, email, password, confirmation]

        for info in user_infos:
            if not info:
                return apology("Please enter all required fields")
            
        if password != confirmation:
            return apology("Passwords do not match")
        
        count = db.execute("SELECT COUNT(*) AS n FROM users \
                           WHERE email = ?", email)
        
        if count[0]["n"] > 0:
            return apology("Email already registered")
        
        db.execute("INSERT INTO users(first_name, last_name, email, hash)\
                   VALUES(?, ?, ?, ?)", 
                   first_name, last_name, email, 
                   generate_password_hash(password))
        
        return redirect("/login")
    
    else:
        return render_template("register.html")

        

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")