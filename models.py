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
