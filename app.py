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
app.jinja_env.filters["two_places"] = two_places

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
    

@app.route("/new_game", methods=["GET", "POST"])
@login_required
def new_game():
    if request.method == "POST":
        if not request.form.get("left_team") or not request.form.get("right_team"):
            flash("Please select two teams.")
            teams = db.execute("SELECT * FROM teams WHERE user_id = ?", session["user_id"])
            return render_template("new_game.html", teams=teams)
        elif request.form.get("left_team") == request.form.get("right_team"):
            flash("Teams must not be the same.")
            teams = db.execute("SELECT * FROM teams WHERE user_id = ?", session["user_id"])
            return render_template("new_game.html", teams=teams)

        game_id = db.execute("INSERT INTO games (user_id, left_team_id, right_team_id) VALUES (?, ?, ?)", session["user_id"],
                             request.form.get("left_team"), request.form.get("right_team"))
        session["game_id"] = game_id
        session["tossup_num"] = 1

        return redirect("/game")

    elif request.method == "GET":
        teams = db.execute("SELECT * FROM teams WHERE user_id = ?", session["user_id"])
        return render_template("new_game.html", teams=teams)

    
@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    if request.method == "POST":
        if "game_id" not in session or "tossup_num" not in session:
            return apology("It appears you do not have a game in progress.", 404)

        bonus = 0
        if request.form.get("b-checkbox-1"):
            bonus += int(request.form.get("b-checkbox-1"))
        if request.form.get("b-checkbox-2"):
            bonus += int(request.form.get("b-checkbox-2"))
        if request.form.get("b-checkbox-3"):
            bonus += int(request.form.get("b-checkbox-3"))

        if request.form.get("scoring-player") and request.form.get("negging-player"):
            if request.form.get("scoring-player") == request.form.get("negging-player"):
                return apology("Scoring player and negging player cannot be the same", 400)

        if request.form.get("score"):
            team_id = db.execute("SELECT team_id FROM players WHERE id = ?", request.form.get("scoring-player"))
            if not team_id:
                return apology("An error occurred", 500)
            else:
                team_id = team_id[0]["team_id"]
            db.execute("INSERT INTO score_events (game_id, team_id, player_id, tossup_num, score, bonus) VALUES (?, ?, ?, ?, ?, ?)", 
                       session["game_id"], team_id, request.form.get("scoring-player"), session["tossup_num"], request.form.get("score"), bonus)
        if request.form.get("neg-score"):
            team_id = db.execute("SELECT team_id FROM players WHERE id = ?", request.form.get("negging-player"))
            if not team_id:
                return apology("An error occurred", 500)
            else:
                team_id = team_id[0]["team_id"]
            db.execute("INSERT INTO score_events (game_id, team_id, player_id, tossup_num, score, bonus) VALUES (?, ?, ?, ?, ?, ?)", 
                       session["game_id"], team_id, request.form.get("negging-player"), session["tossup_num"], request.form.get("neg-score"), 0)

        gamedata = get_gamedata(session["game_id"])
        session["tossup_num"] += 1
        tossup = session["tossup_num"]
        return render_template("game.html", gamedata=gamedata, tossup=tossup)

    elif request.method == "GET":
        gamedata = get_gamedata(session["game_id"])
        tossup = session["tossup_num"]
        return render_template("game.html", gamedata=gamedata, tossup=tossup)


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


def get_gamedata(g_id):
    gamedata = {}
    global db

    l_id = db.execute("SELECT left_team_id FROM games WHERE id = ?", g_id)
    r_id = db.execute("SELECT right_team_id FROM games WHERE id = ?", g_id)
    if not l_id or not r_id:
        return None
    else:
        l_id = l_id[0]["left_team_id"]
        r_id = r_id[0]["right_team_id"]

    l_name = db.execute("SELECT name FROM teams WHERE id = ?", l_id)
    r_name = db.execute("SELECT name FROM teams WHERE id = ?", r_id)
    gamedata["left_name"] = l_name[0]["name"]
    gamedata["right_name"] = r_name[0]["name"]

    left_players = db.execute("SELECT * FROM players WHERE team_id = ?", l_id)
    gamedata["left_players"] = left_players
    right_players = db.execute("SELECT * FROM players WHERE team_id = ?", r_id)
    gamedata["right_players"] = right_players

    left_scores = db.execute("SELECT * FROM score_events WHERE game_id = ? AND team_id = ?", g_id, l_id)
    left_tossups = {}
    left_subscore = 0
    left_ppgs = {}
    left_ppb = [0, 0]
    if left_scores:
        for row in left_scores:
            left_subscore += (row["score"] + row["bonus"])
            left_tossups[row["tossup_num"]] = {"player_id": row["player_id"], "score": row["score"], "bonus": row["bonus"], "subscore": left_subscore}

            if not row["player_id"] in left_ppgs:
                left_ppgs[row["player_id"]] = row["score"]
            else:
                left_ppgs[row["player_id"]] += row["score"]

            if row["score"] > 0:
                left_ppb[0] += row["bonus"]
                left_ppb[1] += 1

    gamedata["left_tossups"] = left_tossups

    for player in left_players:
        pid = player["id"]
        if not pid in left_ppgs:
            left_ppgs[pid] = 0
    gamedata["left_ppgs"] = left_ppgs

    if left_ppb[1] == 0:
        left_ppb = 0
    else:
        left_ppb = left_ppb[0] / left_ppb[1]
    gamedata["left_ppb"] = left_ppb

    gamedata["left_score"] = left_subscore
    
    right_scores = db.execute("SELECT * FROM score_events WHERE game_id = ? AND team_id = ?", g_id, r_id)
    right_tossups = {}
    right_subscore = 0
    right_ppgs = {}
    right_ppb = [0, 0]
    if right_scores:
        for row in right_scores:
            right_subscore += (row["score"] + row["bonus"])
            right_tossups[row["tossup_num"]] = {"player_id": row["player_id"], "score": row["score"], "bonus": row["bonus"], "subscore": right_subscore}

            if not row["player_id"] in right_ppgs:
                right_ppgs[row["player_id"]] = row["score"]
            else:
                right_ppgs[row["player_id"]] += row["score"]

            if row["score"] > 0:
                right_ppb[0] += row["bonus"]
                right_ppb[1] += 1

    gamedata["right_tossups"] = right_tossups

    for player in right_players:
        pid = player["id"]
        if not pid in right_ppgs:
            right_ppgs[pid] = 0
    gamedata["right_ppgs"] = right_ppgs

    if right_ppb[1] == 0:
        right_ppb = 0
    else:
        right_ppb = right_ppb[0] / right_ppb[1]
    gamedata["right_ppb"] = right_ppb

    gamedata["right_score"] = right_subscore

    print(gamedata)
    return gamedata


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
