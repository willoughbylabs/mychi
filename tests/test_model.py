import os, sys
from app import app
from unittest import TestCase
from models import db, Line, Stop

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

app.config["ENV"] == "testing"
db.drop_all()
db.create_all()


class LineModelTestCase(TestCase):
    """ Test for train lines model. """

    def setUp(self):
        """ Delete all existing rows before each test and add one test row. """
        Line.query.delete()
        line = Line(id="blue", name="Blue Line")
        db.session.add(line)
        db.session.commit()
        self.line = line

    def test_add_line(self):
        """ Verify a new line can be added to database. """

        self.assertEqual(self.line.id, "blue")
        self.assertEqual(len(Line.query.all()), 1)
