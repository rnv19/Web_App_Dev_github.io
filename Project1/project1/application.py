import os
import datetime
from dotenv import load_dotenv
from models import Users

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
db.init_app(app)
db = SQLAlchemy(app)

def main():
    db.create_all()
    # Users.__table__.drop(engine)

@app.route("/register", methods=["GET","POST"])
def register():
    print("starting", session)
    if 'username' in session:
        username = session["username"]
        return (f"<h1>Logged in as {username}</h1>" + "<b><a href = '/dropsession'>click here to log out</a></b>")

    if request.method == "GET":
        alert = False
        return render_template("login.html", alert=alert)
    
    elif request.method == "POST":
        if (request.form["button"] == "register"):
            return render_template("registration.html")
        
        elif (request.form["button"] == "submit"):
            name = request.form.get("name")
            username = request.form.get("username")
            password = request.form.get("password")
            birthday = request.form.get("birthday")
            address = request.form.get("address")
            print(name, username, password, birthday, address)
            user = Users(name=name, username=username, password=password, birthday=birthday, address=address)
            try:
                db.session.add(user)
                db.session.commit()
                return (f"User {name} successfully added to database...!")
            except Exception as e:
                return ("Exception raised! Operation was unsucessful...!")
        
        elif (request.form["button"] == "login"):
            username = request.form.get("username")
            password = request.form.get("password")
            res = Users.query.get(username)
            try:
                if (username == res.username):
                    if (password == res.password):
                        print("before login", session)
                        session["username"] = res.username
                        print("after login", session)
                        return render_template("user.html", username = username)
            except Exception as e:
                print(e)
                return render_template("login.html", alert=True)

@app.route("/admin", methods=["GET"])
def admin():
    res = Users.query.all()
    return render_template("admin.html", table=res)

@app.route("/dropsession")
def logout():
    print("before logout", session)
    session.pop('username', None)
    print("after logout", session)
    return ("<h1>Successfully logged out...<h1>" + "<b><a href = '/register'>click here to login again</a></b>")
if __name__ == "__main__":
    with app.app_context():
        main()