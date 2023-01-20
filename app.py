#import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask import jsonify
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from functools import wraps
# create connection to project database sqlite
con = sqlite3.connect("project.db", check_same_thread=False)
cur = con.cursor()


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/turtle", methods=['GET', 'POST'])
@login_required
def turtle():
    turtle = request.form.get("turtle")
    if request.method == "POST":
        # get current users id
        id = session["user_id"]
        # gets the post from user
        turtle = request.form.get("turtle")
        # receives current time in specific format
        time=datetime.now().strftime("%c")
        # turns three variables into a list
        feed = [id, turtle, time]

        # checks to see if post is blank, if it isn't it'll add info into posts databases
        if turtle!="":
            cur.execute("INSERT INTO posts (user_id, feed, time) VALUES (?, ?, ?)", (feed))
            con.commit()
        return redirect("/")
    else:
        return render_template("index.html")

@app.route("/")
@login_required
def index():
    # pulls data from two different databases
    data = list(cur.execute("SELECT posts.feed, posts.time, posts.user_id, users.username FROM posts LEFT JOIN users ON posts.USER_id=users.id WHERE feed IS NOT NULL ORDER BY posts.id DESC"))
    con.commit()
    # takes usernames and ids from users database and turns them into list
    users = list(cur.execute("SELECT username,id FROM users"))
    return render_template("index.html", data=data, username = users)

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Get stock quote."""
    if request.method == "POST":
        # pulls username from users
        username = list(cur.execute("SELECT username FROM users"))
        # finds all usernames in users database
        users = [row[0] for row in username]
        con.commit()
        # current users id
        id = session["user_id"]
        # takes id and finds username from database
        current_user=(list(cur.execute("SELECT username FROM users WHERE id=?", (id,))))[0][0]
        # finds user that current user wants to caht with
        chat_user = request.form.get("user")
        # finds corresponding id from that user from users database
        chat_id = (list(cur.execute("SELECT id FROM users WHERE username = ?", (chat_user,))))[0][0]
        # pulls in chat text from current user
        chat_text = request.form.get("chat_text")
        # receives current time in specific format
        time=datetime.now().strftime("%c")
        # turns four variables into a list
        info = [chat_id, chat_text, id, time]
        # turns four variables into a list
        data_input=[chat_id, current_user, id, chat_user]
        con.commit()
        # does not allow to chat with yourself
        if chat_user == current_user:
            return apology("Cannot chat with yourself")
        # if chat is not empty, it enters data into posts databse
        if chat_text != "":
            cur.execute("INSERT INTO posts (chat_id, chat, user_id, time) VALUES (?, ?, ?, ?)", (info))
            con.commit()
        # pulls updated data to send to html
        data = list(cur.execute("SELECT posts.chat, posts.time, posts.chat_id, users.username FROM posts LEFT JOIN users ON posts.USER_id=users.id WHERE (chat_id=? AND username=?) OR (chat_id=? AND username=?) AND chat IS NOT NULL ORDER BY posts.id DESC", (data_input)))
        return render_template("chatting.html", users=users, data=data, chat_user=chat_user)

    else:
        # finds usernames in database
        username = list(cur.execute("SELECT username FROM users"))
        # loops to pull all users in users database
        users = [row[0] for row in username]
        # finds current login id
        id = session["user_id"]
        # uses id to find current username within users database
        current_user=(list(cur.execute("SELECT username FROM users WHERE id=?", (id,))))[0][0]
        con.commit()
        return render_template("chat.html", users=users)# , data=data)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method=="GET":
        # finds current login id
        id = session["user_id"]
        # selects data from posts from logged in user where feed column is not empty. this eliminates chat converstations and other users psots
        data = list(cur.execute("SELECT feed, time FROM posts WHERE user_id = ? AND feed IS NOT NULL ORDER BY id DESC", (id,)))
        # gets current users username
        username = list(cur.execute("SELECT username FROM users WHERE id = ?", (id,)))
        con.commit()
        return render_template("profile.html", data=data, username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # receives username input from login screen
    username = request.form.get("username")
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for password where username is the same as username input in form
        rows = list(cur.execute("SELECT passhash FROM users WHERE username = ?", (username,)))
        # gets id from users database where username is the same
        id = list(cur.execute("SELECT id FROM users WHERE username = ?", (username,)))
        # receives password from form
        password = request.form.get("password")
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][0], password):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = id[0][0]
        con.commit()
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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # gets username input from form
        username = request.form.get("username")
        # creates hash from password
        hashword = generate_password_hash(request.form.get("password"))
        # creats list from username and password
        login = [username, hashword]
        # selects username from database
        find_user = cur.execute("SELECT * FROM users WHERE username = (?)", (username,))

        # determines if username was entered
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # determines if password matches itself
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)
        # makes sure username isn't already in database
        elif list(find_user) != []:
            return apology("Username already taken")

        # insert username and hashed password into database
        cur.executemany("INSERT INTO users (username, passhash) VALUES(?, ?)", (login,))
        con.commit()

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")