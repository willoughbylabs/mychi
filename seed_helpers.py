import os
import requests
from models import Line, Stop


#  ##### Train Lines #####


def generate_train_lines():
    """ Generates hardcoded list of train lines. """
    red = Line(id="red", name="Red Line")
    blue = Line(id="blue", name="Blue Line")
    brown = Line(id="brn", name="Brown Line")
    green = Line(id="g", name="Green Line")
    orange = Line(id="o", name="Orange Line")
    purple = Line(id="p", name="Purple Line")
    pink = Line(id="pnk", name="Pink Line")
    yellow = Line(id="y", name="Yellow Line")
    # purple_exp = Line(id="pexp", name="Purple Line Express")

    lines_list = [red, blue, brown, green, orange, pink, purple, yellow]
    return lines_list


def generate_stations_list():
    """ Retrieves stations from List of 'L' stops API. """

    stations = []
    url = "https://data.cityofchicago.org/resource/8pix-ypme.json"
    line_ids = ["red", "blue", "brn", "g", "o", "p", "pnk", "y"]
    for line in line_ids:
        params = {"$$app_token": os.environ.get("SOCRATA_KEY", ""), line: "true"}
        response = requests.get(url, params=params).json()
        for station in response:
            new_stop = Stop(
                stop_id=station["stop_id"],
                line_id=line,
                stop_name=station["stop_name"],
                station_name=station["station_name"],
            )
            stations.append(new_stop)
    return stations
