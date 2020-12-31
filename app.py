from flask import Flask, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Line
from forms import TransitTrainForm


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
    form.line.choices = line_choices
    return render_template("transit.html", form=form)


@app.route("/api/lines")
def get_train_lines():
    """ Get list of train lines from database. """

    return redirect(url_for("display_transit_dashboard"))
