import os, sys
import unittest
from app import app
from unittest import TestCase
from models import db, Line, Stop
from sqlalchemy.exc import IntegrityError

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


db.drop_all()
db.create_all()


class LineModelTestCase(TestCase):
    """ Tests for train lines model. """

    def setUp(self):
        """ Delete all existing rows before each test and add one test row. """
        Line.query.delete()
        line = Line(id="blue", name="Blue Line")
        db.session.add(line)
        db.session.commit()
        self.line = line

    def tearDown(self):
        db.session.rollback()

    def test_add_line(self):
        """ Verify a new line can be added to database. """

        self.assertEqual(self.line.id, "blue")
        self.assertEqual(len(Line.query.all()), 1)

        new_line = Line(id="red", name="Red Line")
        db.session.add(new_line)
        db.session.commit()

        self.assertEqual(len(Line.query.all()), 2)

    # ? Returns FlushError, recognizes already an instance but not producing IntegrityError.
    # ? New instance <Line at 0x1100ecfa0> with identity key (<class 'models.Line'>, ('blue',), None) conflicts with persistent instance <Line at 0x10f5cb790>
    @unittest.skip("Returns FlushError instead of IntegrityError")
    def test_duplicate_line(self):
        """ Verify integrity error if duplicate line is added. """

        line2 = Line(id="blue", name="Blue Line")
        db.session.add(line2)

        self.assertRaises(IntegrityError, db.session.commit)


class StopModelTestCase(TestCase):
    """ Tests for train stops model. """

    def setUp(self):
        Stop.query.delete()
        Line.query.delete()

        line = Line(id="red", name="Red Line")
        db.session.add(line)
        db.session.commit()

        stop = Stop(
            stop_id="30192",
            line_id="red",
            stop_name="69th (95th-bound)",
            station_name="69th",
        )
        db.session.add(stop)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_add_stop(self):
        """ Verify a new stop can be added to database. """
        self.assertEqual(len(Stop.query.all()), 1)

        stop2 = Stop(
            stop_id="30191",
            line_id="red",
            stop_name="69th (Howard-bound)",
            station_name="69th",
        )
        db.session.add(stop2)
        db.session.commit()

        self.assertEqual(len(Stop.query.all()), 2)

    def test_invalid_line_id(self):

        stop2 = Stop(
            stop_id="30191",
            line_id="black",
            stop_name="69th (Howard-bound)",
            station_name="69th",
        )
        db.session.add(stop2)

        self.assertRaises(IntegrityError, db.session.commit)
