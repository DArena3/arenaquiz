import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, two_places

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["2places"] = two_places

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///records.db")


@app.route("/", methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide a username.")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide a password.")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Logged in successfully.")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Please provide a username.")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Please provide a password.")
            return render_template("register.html")
        elif not request.form.get("confirmation"):
            flash("Please confirm your password.")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Both passwords must match.")
            return render_template("register.html")
        else:
            # Duplicate username creates an exception due to the "UNIQUE" constraint on the username field
            try:
                added = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                   request.form.get("username"), generate_password_hash(request.form.get("password")))
            except (RuntimeError, ValueError):
                flash("Username already exists.")
                return render_template("register.html")

            session["user_id"] = added

            flash("Thank you for joining ArenaQuiz!")
            return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/teams", methods=["GET", "POST"])
@login_required
def teams():
    if request.method == "POST":
        if not request.form.get("team"):
            flash("Please select a team.")
            teams = db.execute("SELECT * FROM teams WHERE user_id = ?", session["user_id"])
            return render_template("teams.html", teams=teams)
        
        return redirect("/viewteam?team_id=" + request.form.get("team"))

    elif request.method == "GET":
        teams = db.execute("SELECT * FROM teams WHERE user_id = ?", session["user_id"])
        return render_template("teams.html", teams=teams)


@app.route("/viewteam", methods=["GET"])
@login_required
def view_team():
    if request.method == "GET":
        name = db.execute("SELECT name FROM teams WHERE user_id = ? AND id = ?", session["user_id"], request.args.get("team_id"))
        if not name:
            return apology("Team not found", 404)
        players = db.execute("SELECT name FROM players WHERE user_id = ? AND team_id = ?", session["user_id"], request.args.get("team_id"))
        return render_template("viewteam.html", name=name[0]['name'], players=players)


@app.route("/add_team", methods=["GET", "POST"])
@login_required
def add_team():
    if request.method == "POST":
        if not request.form.get("tname"):
            flash("Please enter a team name.")
            return render_template("add_team.html")

        names = []
        for i in range(1,9):
            if request.form.get("player" + str(i)):
                names.append(request.form.get("player" + str(i)))
        if not names:
            flash("Team must have at least one player.")
            return render_template("add_team.html")

        team_id = db.execute("INSERT INTO teams (user_id, name) VALUES (?, ?)", session["user_id"], request.form.get("tname"))

        for name in names:
            db.execute("INSERT INTO players (user_id, name, team_id) VALUES (?, ?, ?)", session["user_id"], name, team_id)

        flash("Successfully added team: " + request.form.get("tname") + ".")
        return redirect("/teams")

    elif request.method == "GET":
        return render_template("add_team.html")
    
    
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # Change password
    
    # Input validation
    if request.method == "POST":
        if not request.form.get("old_password"):
            flash("Please enter your current password.")
            return render_template("change_password.html")
        elif not request.form.get("new_password"):
            flash("Please enter the new password.")
            return render_template("change_password.html")
        elif not request.form.get("confirmation"):
            flash("Please confirm your new password.")
            return render_template("change_password.html")
        elif request.form.get("new_password") != request.form.get("confirmation"):
            flash("Both new passwords must match.")
            return render_template("change_password.html")
        else:
            rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
            if not rows:
                flash("An error occurred.")
                return render_template("change_password.html")
            elif not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
                flash("Invalid password.")
                return render_template("change_password.html")
            # Update password
            db.execute("UPDATE users SET hash = ? WHERE id = ?",
                       generate_password_hash(request.form.get("new_password")), session["user_id"])

            flash("Password updated successfully.")
            return redirect("/")

    elif request.method == "GET":
        return render_template("change_password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
