import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    tot = 0

    dtb = db.execute("SELECT cash FROM users WHERE username = ?",session['username'])
    dtb2 = db.execute("SELECT DISTINCT symbol, SUM(shares_number) AS quantidade FROM shares WHERE user_id = ? GROUP BY symbol",session['user_id'])
    data = [lookup(dtb2[c]['symbol']) for c in range(len(dtb2))]

    for c in range(len(dtb2)):
        data[c]['quantity'] = dtb2[c]['quantidade']
        tot += (dtb2[c]['quantidade'] * data[c]['price'])
        data[c]['total'] = dtb2[c]['quantidade'] * data[c]['price']
        data[c]['price'] = data[c]['price']

    tot += dtb[0]['cash']
    tot = tot
    dtb[0]['cash'] = dtb[0]['cash']


    return render_template("index.html",money = dtb[0]['cash'], info_shares = data, quant = len(data), total = tot)

    #  users_db = dtb, shares_db = dtb2, info_shares = info_share, quantity = qnt

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_info = db.execute("SELECT * FROM users WHERE id = ?",session['user_id'])
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        elif lookup(request.form.get("symbol")) == None:
                return apology("Invalid symbol", 400)

        if not request.form.get("shares"):
            return apology("Missing shares", 400)

        if not request.form.get("shares").isdigit():
            return apology("Just positive integer values")
        if not float(request.form.get("shares")) > 0:
            return apology("Just positive integer values")


        share = lookup(request.form.get("symbol"))
        share_price = float(share['price'])
        cash = user_info[0]['cash'] - (share_price * float(request.form.get("shares")))

        if (share_price * float(request.form.get("shares"))) > user_info[0]['cash']:
            return apology("Can't afford", 400)

        db.execute("INSERT INTO shares(user_id, symbol, shares_number, transacted) VALUES (?, ?, ?, ?)", session['user_id'], request.form.get("symbol"), request.form.get("shares"), str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        db.execute("UPDATE users SET cash = ? WHERE id = ? LIMIT 1", cash, session['user_id'])
        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    shares = db.execute("SELECT symbol, shares_number, transacted FROM shares WHERE user_id = ?", session['user_id'])
    for c in range(len(shares)):
        info = lookup(shares[c]['symbol'])
        shares[c]['price'] = info['price'] * shares[c]['shares_number']
        if shares[c]['price'] < 0 :
            shares[c]['price'] *= -1

    return render_template("history.html", shares = shares, qnt = len(shares))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]['username']

        # Redirect user to home page
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        else:
            if lookup(request.form.get("symbol")) == None:
                return apology("Invalid symbol", 400)

        symbol = lookup(request.form.get("symbol"))
        return render_template("quoted.html",symbol = symbol)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)
        else:
            query = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            if len(query) != 0:
                return apology("Username is not available!")

        if not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm the password", 400)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("the passwords don't matchs", 400)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        query = db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, password)

        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        user_info = db.execute("SELECT * FROM users WHERE id = ?",session['user_id'])
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        if not request.form.get("shares"):
            return apology("Missing shares", 400)
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        shares_info = db.execute("SELECT sum(shares_number) AS qnt FROM shares WHERE user_id = ? AND symbol = ?", session['user_id'], symbol)
        share = lookup(symbol)
        share = float(share['price'])
        cash = user_info[0]['cash'] + (share * float(shares))

        if int(shares) > shares_info[0]['qnt']:
            return apology("Too many shares", 400)

        db.execute("INSERT INTO shares(user_id, symbol, shares_number, transacted) VALUES (?, ?, ?, ?)", session['user_id'], symbol, int(shares) * -1, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        db.execute("UPDATE users SET cash = ? WHERE id = ? LIMIT 1",cash , session['user_id'])
        flash("Sold!")
        return redirect("/")

    else:
        symbols = db.execute("SELECT DISTINCT symbol FROM shares where user_id = ?", session["user_id"])

        return render_template("sell.html", symbols = symbols, qnt = len(symbols))


@app.route("/change_password", methods = ["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        if not request.form.get("new-password"):
            return apology("must provide a new password", 400)

        elif not request.form.get("new-confirmation"):
            return apology("must confirm the new password", 400)
        elif request.form.get("new-password") != request.form.get("new-confirmation"):
            return apology("the passwords don't matchs", 400)

        senha = request.form.get("new-password")
        db.execute("UPDATE users SET hash = ? WHERE id = ? LIMIT 1", generate_password_hash(senha), session['user_id'])
        return logout()

    else:
        return render_template("change_password.html")