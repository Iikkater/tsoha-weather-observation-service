import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.String(20), default='basic', nullable=False)

def generate_unique_id():
    while True:
        new_id = random.randint(10000000, 99999999)
        if not User.query.get(new_id):
            return new_id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        found_user = User.query.filter_by(username=username).first()

        if found_user and found_user.tier != 'locked' and check_password_hash(found_user.password, password):
            session["username"] = username
            session["tier"] = found_user.tier
            return redirect(url_for("user"))
        
        if found_user and found_user.tier == 'locked':
            flash("Tilisi on lukittu. Ota yhteyttä ylläpitoon.", "login")
        else:
            flash("Virheellinen käyttäjätunnus tai salasana. Yritä uudelleen.", "login")
        return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        retype_password = request.form["retype_password"]
        tier = "basic"  # Set tier to basic by default

        if password != retype_password:
            flash("Salasanat eivät täsmää. Yritä uudelleen.")
            return redirect(url_for("create_account"))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash("Käyttäjätunnus tai sähköpostiosoite on jo käytössä. Valitse toinen.")
            return redirect(url_for("create_account"))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(id=generate_unique_id(), firstname=firstname, surname=surname, email=email, username=username, password=hashed_password, tier=tier)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("create_account.html")

@app.route("/user")
def user():
    if "username" in session:
        return render_template("user.html")

    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("tier", None)
    return redirect(url_for("index"))

@app.route("/change_tier", methods=["POST"])
def change_tier():
    if "username" not in session or session["tier"] != "admin":
        flash("Sinulla ei ole oikeuksia muuttaa käyttäjätasoja.", "change_tier")
        return redirect(url_for("user"))

    username = request.form["username"]
    new_tier = request.form["tier"]

    if username == session["username"]:
        flash("Et voi muuttaa omaa käyttäjätasoasi.", "change_tier")
        return redirect(url_for("user"))

    current_user = User.query.filter_by(username=username).first()
    if current_user:
        current_user.tier = new_tier
        db.session.commit()
        flash("Käyttäjätaso muutettu onnistuneesti.", "change_tier")
    else:
        flash("Käyttäjää ei löytynyt.", "change_tier")

    return redirect(url_for("user"))

@app.route("/search_users", methods=["GET"])
def search_users():
    query = request.args.get("q", "")
    users = User.query.filter(User.username.ilike(f"{query}%")).all()
    user_list = [{"username": user.username} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)
