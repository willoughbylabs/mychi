import os
import requests

# from keys import train_tracker_key


def get_prediction(stop_id, line_id):
    """ Retrieve arrival prediction for a """

    if line_id == "o":
        line_id = "org"
    if line_id == "pnk":
        line_id = "pink"
        # TODO: add error handling
    url = "https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?"
    response = requests.get(
        f"{url}key={os.environ.get('TRAIN_TRACKER_KEY', train_tracker_key)}&stpid={stop_id}&rt={line_id}&outputType=JSON"
    )
    return response.json()


def add_prediction_to_session(savedPrdt, session):
    """ Add a saved prediction to session storage. """

    new_session = session["savedStops"]
    new_session.append(savedPrdt["data"])
    session["savedStops"] = new_session


def delete_prediction_from_session(savedPrdt, session):
    """ Delete a saved prediction from session storage. """

    line = savedPrdt["line"]
    stop = savedPrdt["stop"]
    search_for = {"line": line, "stop": stop}
    new_session = session["savedStops"]
    index = new_session.index(search_for)
    new_session.pop(index)
    session["savedStops"] = new_session
