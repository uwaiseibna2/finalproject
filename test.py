import unittest
from app import app, db, User
from flask_login import current_user
import random
import os
class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['TESTING'] = True
        app = Flask(__name__)
        app.secret_key = os.environ.get("FLASK_SECRET_KEY")  # Load secret key from environment variable

        # Database configuration
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASS")
        db_name = os.environ.get("DB_NAME")
        cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

        # Adjust the cloud SQL connection settings
        db_host = '/cloudsql/' + cloud_sql_connection_name  # Cloud SQL Proxy connection
        db_uri = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
        # Update the configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.create_all()

        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        x=str(random.randint(30,45))
        with app.test_request_context():
            # Register a new user
            response = self.app.post('/register', data=dict(
                username='testuser'+x,
                password='testpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Log in with the registered user
            response = self.app.post('/login', data=dict(
                username='testuser'+x,
                password='testpassword'
            ), follow_redirects=True)
            self.assertIn(b'Image Gallery', response.data)
            self.assertEqual(current_user.username, ('testuser'+x))

    
if __name__ == '__main__':
    unittest.main()
