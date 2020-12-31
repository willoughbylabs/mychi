from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)


class Line(db.Model):
    """ Table to store lines and their identifiers. """

    __tablename__ = "lines"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """ Represent model object as line ID and name. """

        line = self
        return f"<Line ID: {line.id} - {line.name}>"


class Stop(db.Model):
    """ Table to store train stops. """

    __tablename__ = "stops"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stop_id = db.Column(db.Integer, nullable=False)
    line_id = db.Column(db.String, db.ForeignKey("lines.id"), nullable=False)
    stop_name = db.Column(db.String, nullable=False)
    station_name = db.Column(db.String, nullable=False)

    line = db.relationship("Line", backref="stops")

    def generate_stations(line_id):
        """ Generate a list of stations for a given train line. """

        stations = []
        stations_db = (
            db.session.query(Stop.station_name)
            .filter_by(line_id=line_id)
            .group_by(Stop.station_name)
            .all()
        )
        for station in stations_db:
            stations.append(Stop.station_to_dictionary(station))
        return stations

    def station_to_dictionary(station):
        """ Convert data into dictionary for conversion into JSON. """

        station_dict = {"station_name": station.station_name}
        return station_dict

    def __repr__(self):
        """ Represent stop with line_id and stop name. """

        stop = self
        return f"<Stop: Line ID: {stop.line_id}, Station: {stop.stop_name}>"
