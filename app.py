import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
db = SQL("sqlite:///iquit.db")

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
def add():
    if request.method == "POST":

        habits_list = db.execute("SELECT habit FROM habits WHERE user_id = ?", session["user_id"])
        habit = request.form.get("habit")

        if not habit:
            return apology("Please enter a habit")
 
        if habit == "Others":
            habit = request.form.get("others")
        
        # Make sure same habit did not get registered twice
        for row in habits_list:
            if habit == row["habit"]:
                return apology("Habit already registered", 403)

        starting_streak = 0
        todays_date = datetime.datetime.now().date()
        db.execute(
            "INSERT INTO habits(user_id, habit, start_time, enter_time, streak) VALUES(?, ?, ?, ?, ?)",
            session["user_id"],
            habit,
            todays_date,
            todays_date,
            starting_streak,
        )

        return redirect("/dashboard")

    else:
        common_habits = [
            "Smoking",
            "Gambling",
            "Drinking alcohol",
            "Drug use",
            "Poor diet",
            "Social media scrolling",
            "Others",
        ]
        return render_template("add.html", common_habits=common_habits)


@app.route("/dashboard")
@login_required
def dashboard():

    habits = db.execute(
        "SELECT * FROM habits\
                        WHERE user_id = ?",
        session["user_id"],
    )

    return render_template("dashboard.html", habits=habits)


@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    if request.method == "POST":
        daily_habits = request.form.getlist("habit")

        for habit in daily_habits:
            db.execute(
                "UPDATE habits SET streak = streak + 1, enter_time = ?\
                WHERE habit = ?",
                datetime.datetime.now().date(),
                habit,
            )

        return redirect("/dashboard")

    else:

        habits = db.execute(
            "SELECT habit FROM habits WHERE user_id = ?", session["user_id"]
        )
        friends_list = db.execute("SELECT first_name, last_name, id FROM users WHERE id IN \
                                 (SELECT member2id FROM friendships WHERE member1id = ?)", session["user_id"])
        if not habits:
            return redirect("/add")
        
        # Commented for testing
        """for row in habits:
            # SQLite store as string: has to convert to correct object for comparison
            if (
            datetime.datetime.strptime(row["enter_time"], "%Y-%m-%d").date()
            == datetime.datetime.now().date()
            ):
                return apology("Today's work is done", 403)

        else:"""
        return render_template("tracker.html", habits=habits, friends_list=friends_list)

@app.route("/leaderboard")
@login_required
def leaderboard():
    leaders = db.execute("SELECT * FROM scores LIMIT 30\
                         ORDER BY score DESC")
    return render_template("leaderboard.html", leaders=leaders)

@app.route("/search")
def search():
    q = request.args.get("q")
    info = db.execute("SELECT * FROM users WHERE email = ?", q)
    user_info = info[0]
    if user_info:
        return jsonify(info)

@app.route("/friends")
def friends():
    friends = db.execute("SELECT * FROM users WHERE id IN\
                         (SELECT member2id FROM friendships\
                         WHERE member1id = ?)", session["user_id"])
    return render_template("friends.html", friends=friends)

@app.route("/addfriend", methods=["GET", "POST"])
def addfriend():
    if request.method == "GET": 
        return render_template("addfriend.html")
    else: 
        id = request.form.get("id")
        db.execute("INSERT INTO friendships (member1id, member2id) VALUES(?, ?)", session["user_id"], id)
        return redirect("/friends")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not (email := request.form.get("email")):
            return apology("Please enter Email")
        if not request.form.get("password"):
            return apology("Please enter a password")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

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

        count = db.execute(
            "SELECT COUNT(*) AS n FROM users \
                           WHERE email = ?",
            email,
        )

        if count[0]["n"] > 0:
            return apology("Username already registered")

        db.execute(
            "INSERT INTO users(first_name, last_name, email, hash)\
                   VALUES(?, ?, ?, ?)",
            first_name,
            last_name,
            email,
            generate_password_hash(password),
        )

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
