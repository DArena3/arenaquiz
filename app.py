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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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
            return apology("Please enter a username.", 400)
        elif not request.form.get("password"):
            return apology("Please enter a password.", 400)
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password.", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords don't match.", 400)
        else:
            # Duplicate username creates an exception due to the "UNIQUE" constraint on the username field
            try:
                added = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                   request.form.get("username"), generate_password_hash(request.form.get("password")))
            except (RuntimeError, ValueError):
                return apology("Username already in use", 400)

            session["user_id"] = added

            return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/teams")
@login_required
def teams():
    # TODO
    pass
    
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # Change password
    
    # Input validation
    if request.method == "POST":
        if not request.form.get("old_password"):
            return apology("Enter current password", 400)
        elif not request.form.get("new_password"):
            return apology("Enter new password", 400)
        elif not request.form.get("confirmation"):
            return apology("Confirm Password", 400)
        elif request.form.get("new_password") != request.form.get("confirmation"):
            return apology("The passwords don't match.", 400)
        else:
            rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
            if rows == []:
                return apology("An error occurred", 400)
            elif not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
                return apology("Password invalid", 403)
            # Update password
            db.execute("UPDATE users SET hash = ? WHERE id = ?",
                       generate_password_hash(request.form.get("new_password")), session["user_id"])

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
