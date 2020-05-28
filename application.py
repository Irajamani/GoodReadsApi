import os
import requests
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():        
    return render_template("index.html", message = False)

@app.route("/success", methods=["POST"])
def success():
    username = request.form["username"]
    password = request.form["password"]
    if db.execute("SELECT * FROM login WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount == 0:
        return render_template("index.html", message = True)
    else:
        a = db.execute("SELECT id from login where username = :username", {"username" : username}).fetchone()
        session["user_id"] = a.id
        return render_template("success.html", message = False)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html", message = False)

@app.route("/validate", methods =["POST"])
def validate():
    username = request.form["username"]
    password = request.form["password"]
    if db.execute("SELECT * FROM login WHERE username = :username", {"username": username}).rowcount > 0:
        return render_template("signup.html", message = True)
    else:
        db.execute("INSERT INTO login (username, password) VALUES (:username, :password)", {"username":username, "password":password})
        db.commit()
        return render_template("success.html")

@app.route("/search", methods = ["POST"])
def search():
    isbn = request.form["isbn"]
    title = request.form["title"]
    author = request.form["author"]
    if isbn is None and title is None and author is None:
        return render_template("success.html", message = True)
    else:
        if len(isbn) > 0:
            q = f"SELECT * FROM books WHERE idnumber LIKE '%{isbn}%'"
            a = db.execute(q).fetchall()
            return render_template("search.html", a = a, isbn = len(isbn))
        elif len(title) > 0:
            q = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
            a = db.execute(q).fetchall()
            return render_template("search.html", a = a, isbn = "2")
        elif len(author) > 0:
            q = f"SELECT * FROM books WHERE author LIKE '%{author}%'"
            a = db.execute(q).fetchall()
            return render_template("search.html", a = a, isbn = "3")
        
@app.route("/specific/<string:number>")
def specific(number):
    a = db.execute("SELECT * FROM books where idnumber = :number", {"number" : number}).fetchone()
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XwYQWnjwXud2OwR7fELZg", "isbns":a.idnumber})
    details = goodreads.json()
    avgrating = details['books'][0]['average_rating']
    norating = details['books'][0]['work_ratings_count']
    return render_template("specific.html", book = a, avgrating = avgrating, norating = norating)
