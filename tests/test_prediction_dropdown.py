import os, sys
from app import app
from unittest import TestCase
from models import db, Line, Stop

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

db.drop_all()
db.create_all()


class TestPredictionDropdown(TestCase):
    """ Test dynamic dropdown routes for transit prediction. """

    def setUp(self):
        """ Add a new line and stop for each test. """

        self.client = app.test_client()
        line = Line(id="red", name="Red Line")
        db.session.add(line)
        db.session.commit()
        self.line = line

        stop = Stop(
            stop_id="30191",
            line_id="red",
            stop_name="69th (Howard-bound)",
            station_name="69th",
        )
        db.session.add(stop)
        db.session.commit()
        self.stop = stop

    def test_display_stations(self):
        """ Test a station is added to the dropdown for the selected line. """

        with self.client as client:
            response = client.get("/api/red/stations")
            data = response.json

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, {"stations": [{"station_name": "69th"}]})

    def test_display_direction(self):
        """ Test a stop direction is added to the dropdown for the selected station. """

        with self.client as client:
            response = client.get(
                "/api/stops",
                query_string=dict(station=self.stop.station_name, line=self.line.id),
            )
            data = response.json

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                data,
                {
                    "stops": [
                        {
                            "stop_id": 30191,
                            "stop_name": "69th (Howard-bound)",
                        }
                    ]
                },
            )
