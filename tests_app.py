from unittest import TestCase
from flask import Flask
from models import db, User

class TestBloglyApp(TestCase):
    def setUp(self):
        """Set up the app for testing."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ECHO'] = False

        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()
            user1 = User(first_name='John', last_name='Doe', image_url='example.jpg')
            user2 = User(first_name='Jane', last_name='Doe', image_url='example.jpg')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    def tearDown(self):
        """Clean up after testing."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_redirect(self):
        """Test the home route redirection."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_list_users(self):
        """Test the route to list all users."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)  #Check if users list page loads
        self.assertIn(b'John Doe', response.data)  #Check if user data is present
        self.assertIn(b'Jane Doe', response.data)  #Check if user data is present

    def test_add_user(self):
        """Test adding a new user."""
        data = {'first_name': 'Alice', 'last_name': 'Smith', 'image_url': 'example.jpg'}
        response = self.client.post('/users/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  #Check if user added
        self.assertIn(b'Alice Smith', response.data)  #Check if added user is present

    def test_user_details(self):
        """Test user details route."""
        user_id = 1  # Assuming user ID 1 exists
        response = self.client.get(f'/user/{user_id}')
        self.assertEqual(response.status_code, 200)  #Check if user details page loads
        self.assertIn(b'John Doe', response.data)  #Check if correct user details are present
