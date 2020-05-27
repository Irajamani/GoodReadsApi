import os

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
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    username = request.form["username"]
    password = request.form["password"]
    if db.execute("SELECT * FROM login WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount == 0:
        return render_template("success.html", username = "Error", password = "Error")
    else:
        return render_template("success.html", username = username, password = password)
