import os, sys
from app import app
from unittest import TestCase

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


class LandingViewsTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        """ Test that home page displays correctly. """

        with self.client as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h3 class="my-3 text-primary">A Concise Data Dashboard</h3>', html
            )

    def test_about_page(self):
        """ Test that about page displays correctly. """

        with self.client as client:
            response = client.get("/about")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<div id="about" class="text-center mt-5">', html)
