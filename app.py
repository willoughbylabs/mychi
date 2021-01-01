from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from operator import itemgetter
from models import db, connect_db, Line, Stop
from forms import TransitTrainForm
from app_helpers import get_prediction


app = Flask(__name__)

# Set Flask configurations based on Flask environment.
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# Connect to database.
connect_db(app)
toolbar = DebugToolbarExtension(app)


@app.route("/")
def display_home_page():
    """ Display welcome page with synopsis of website. """

    return render_template("base.html")


@app.route("/transit")
def display_transit_dashboard():
    """ Display form and dashboard for monitoring arrival predictions for train stops. """

    form = TransitTrainForm()
    lines = Line.query.all()
    line_choices = [(line.id, line.name) for line in lines]
    line_choices.insert(0, ("", "Choose..."))
    form.line.choices = line_choices

    return render_template("transit.html", form=form)


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
    print("****************")
    print(response)
    return f"Getting prediction for {stop_id} on {line_id}"
