from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from flask_debugtoolbar import DebugToolbarExtension
from operator import itemgetter
from models import db, connect_db, Line, Stop
from forms import TransitTrainForm
from app_helpers import (
    get_prediction,
    add_prediction_to_session,
    delete_prediction_from_session,
)

# Configure application.
app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

# Set Flask configurations based on Flask environment.
# ? How am I able to set DATABASE_URI for unittesting?
# ? If I set `export FLASK_ENV=testing`, unittest seems to use a different ENV and not trigger the "testing" if statement. If unittest uses "production" ENV, how to differentiate between production and a unittest?
# if app.config["ENV"] == "testing":
#     app.config.from_object("config.TestingConfig")
# if app.config["ENV"] == "development":
#     app.config.from_object("config.DevelopmentConfig")
# if app.config["ENV"] == "production":
#     app.config.from_object("config.Config")

# Connect to database.
connect_db(app)
toolbar = DebugToolbarExtension(app)


@app.route("/")
def display_home_page():
    """ Display welcome page and message. """

    return render_template("welcome.html")


@app.route("/about")
def display_about_page():
    """ Displays page with synopsis about the application. """

    return render_template("about.html")


@app.route("/transit", methods=["GET", "POST", "DELETE"])
def display_transit_dashboard():
    """ GET: Display form and dashboard for monitoring arrival predictions for train stops. POST: Add saved stop to session storage. DELETE: Remove saved stop from session storage. """

    if request.method == "GET":
        # session["savedStops"] = []
        if "savedStops" not in session:
            session["savedStops"] = []

        form = TransitTrainForm()
        lines = Line.query.all()
        line_choices = [(line.id, line.name) for line in lines]
        line_choices.insert(0, ("", "Choose..."))
        form.line.choices = line_choices

        if len(session["savedStops"]) == 0:
            return render_template("transit.html", form=form)
        else:
            return render_template(
                "transit.html", form=form, savedStops=session["savedStops"]
            )

    if request.method == "POST":
        savedPrdt = request.json
        add_prediction_to_session(savedPrdt, session)
        return "Adding to session."

    if request.method == "DELETE":
        savedPrdt = request.json
        delete_prediction_from_session(savedPrdt, session)
        return "Deleting from session."


@app.route("/api/<line_id>/stations")
def get_stations(line_id):
    """ Get list of stations for a particular line from database. """

    stations_db = Stop.generate_stations(line_id)
    stations = sorted(stations_db, key=itemgetter("station_name"))

    return jsonify(stations=stations)


@app.route("/api/stops")
def get_stops():
    """ Get stops (direction) for a particular line and station. """

    line_id = request.args["line"]
    station_name = request.args["station"]
    stops_db = Stop.generate_stops(line_id, station_name)
    stops = sorted(stops_db, key=itemgetter("stop_name"))

    return jsonify(stops=stops)


@app.route("/transit/prediction")
def get_arrival_prediction():
    """ Get arrival prediction for a provided stop ID. """

    stop_id = request.args["stopID"]
    line_id = request.args["line"]
    response = get_prediction(stop_id, line_id)
    return response
