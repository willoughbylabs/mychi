from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db


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
