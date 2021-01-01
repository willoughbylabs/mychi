import requests
from keys import train_tracker_key


def get_prediction(stop_id, line_id):
    """ Retrieve arrival prediction for a """

    url = "https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?"
    response = requests.get(
        f"{url}key={train_tracker_key}&stpid={stop_id}&rt={line_id}&outputType=JSON"
    )
    return response.json()
