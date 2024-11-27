import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from crypt import verify_password
from db import Database
from queries import Queries

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")

db = Database()
db.connect(app)
queries = Queries(db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        found_user = queries.get_user_by_username(username)

        if found_user and found_user['tier'] != 'locked' and verify_password(password, found_user['password']):
            session["username"] = found_user['username']
            session["tier"] = found_user['tier']
            return redirect(url_for("user"))
        
        if found_user and found_user['tier'] == 'locked':
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

        existing_user = queries.get_user_by_username_or_email(username, email)

        if existing_user:
            flash("Käyttäjätunnus tai sähköpostiosoite on jo käytössä. Valitse toinen.")
            return redirect(url_for("create_account"))

        queries.create_user(firstname, surname, email, username, password, tier)

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

    current_user = queries.get_user_by_username(username)
    if current_user:
        queries.update_user_tier(username, new_tier)
        flash("Käyttäjätaso muutettu onnistuneesti.", "change_tier")
    else:
        flash("Käyttäjää ei löytynyt.", "change_tier")

    return redirect(url_for("user"))

@app.route("/search_users", methods=["GET"])
def search_users():
    query = request.args.get("q", "")
    users = queries.search_users(query)
    user_list = [{"username": user['username']} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)
