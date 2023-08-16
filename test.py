import unittest
from flask import Flask, request
from your_app import app, db  # Assuming your app instance and db are imported
from models import User  # Import the User model

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory database for testing
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Expect a redirect

    def test_list_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)  # Expect successful response

    def test_show_user_form(self):
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)  # Expect successful response

    def test_create_users(self):
        data = {
            "First Name": "John",
            "Last Name": "Doe",
            "Image URL": "http://example.com/image.jpg"
        }
        response = self.client.post('/users/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect successful response

    # You can add more tests as needed

if __name__ == '__main__':
    unittest.main()
