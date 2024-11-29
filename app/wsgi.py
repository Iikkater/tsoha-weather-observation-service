import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from crypt import verify_password
from db import Database
from queries import Queries
from import_postal_areas import import_postal_areas
from check_data import check_observation_data
import pytz

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")

db = Database()
db.connect(app)
queries = Queries(db)

# Import postal areas data
csv_file_path = os.path.join('data/locations', 'Uusimaa_postal_areas.csv')
if not import_postal_areas(csv_file_path):
    print("Error: Failed to import postal areas data.")

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
            session["user_id"] = found_user['id']
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
    session.pop("user_id", None)
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

@app.route("/add_observation", methods=["GET", "POST"])
def add_observation():
    if request.method == "POST":
        user_id = session.get("user_id")
        postal_area_id = request.form["postal_area_id"]
        temperature = request.form.get("temperature", type=float)
        cloudiness = request.form.get("cloudiness", type=int)
        precipitation_amount = request.form.get("precipitation_amount", type=int)
        precipitation_type = request.form.get("precipitation_type", type=int)
        finland = pytz.timezone("Europe/Helsinki")
        observation_time = datetime.now(finland)

        # Tarkista datan oikeellisuus
        errors = check_observation_data(temperature, cloudiness, precipitation_amount, precipitation_type)
        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for("add_observation"))

        queries.add_observation(user_id, postal_area_id, temperature, cloudiness, precipitation_amount, precipitation_type, observation_time)
        flash("Havainto lisätty onnistuneesti.")
        return redirect(url_for("add_observation"))

    parameters = queries.get_parameters()
    postal_areas = queries.get_postal_areas()
    return render_template("add_observation.html", parameters=parameters, postal_areas=postal_areas)

@app.route("/find_data", methods=["GET", "POST"])
def find_data():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        user_id = session.get("user_id")
        tier = session.get("tier")
        start_date_str = request.form["start_date"]
        start_time_str = request.form.get("start_time")
        end_date_str = request.form.get("end_date")
        end_time_str = request.form.get("end_time")
        postal_code = request.form.get("postal_code")

        # Aseta oletusarvot, jos kentät ovat tyhjiä
        if not start_time_str:
            start_time_str = "00:00"
        if not end_date_str:
            end_date_str = start_date_str
        if not end_time_str:
            end_time_str = "23:59"

        # Muunna päivämäärät ja ajat datetime-objekteiksi
        finland = pytz.timezone('Europe/Helsinki')
        start_datetime_str = f"{start_date_str} {start_time_str}"
        end_datetime_str = f"{end_date_str} {end_time_str}"
        try:
            start_time = finland.localize(datetime.strptime(start_datetime_str, '%d-%m-%Y %H:%M'))
            end_time = finland.localize(datetime.strptime(end_datetime_str, '%d-%m-%Y %H:%M'))
        except ValueError as e:
            flash(f"Virheellinen päivämäärä tai kellonaika: {e}")
            return redirect(url_for("find_data"))

        observations = queries.get_observations(user_id, tier, start_time, end_time, postal_code)
        return render_template("find_data.html", observations=observations)

    return render_template("find_data.html", observations=[])

if __name__ == '__main__':
    app.run(debug=True)
