from urllib.parse import urlparse, urljoin

from flask_testing import TestCase
from flask import current_app, url_for
from app.firestore_service import db

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    def test_hello_get(self):
        response = self.client.get(url_for('hello'))

        self.assert200(response)

    def test_hello_post(self):
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))

    def test_auth_signup_get(self):
        response = self.client.get(url_for('auth.signup'))

        self.assert200(response)

    def test_auth_signup_post(self):
        try:
            fake_form = {
                'username': 'test_user1',
                'password': '123456'
            }
            response = self.client.post(url_for('auth.signup'), data=fake_form)
            self.assertRedirects(response, url_for('hello'))
        finally:
            # Remove added db
            db.collection('users').document(fake_form['username']).delete()
    def assertRedirects(self, response, location, message=None):
        """
        Checks if response is an HTTP redirect to the
        given location.

        :param response: Flask response
        :param location: relative URL path to SERVER_NAME or an absolute URL
        """
        parts_location = urlparse(location)

        valid_status_codes = (301, 302, 303, 305, 307)
        valid_status_code_str = ', '.join(str(code) for code in valid_status_codes)
        not_redirect = "HTTP Status %s expected but got %d" % (valid_status_code_str, response.status_code)
        self.assertTrue(response.status_code in valid_status_codes, message or not_redirect)

        if parts_location.netloc:
            expected_location = location
        else:
            server_name = self.app.config.get('SERVER_NAME') or 'localhost'
            expected_location = urljoin("http://%s" % server_name, location)
            # expected_location = location

        parts_response = urlparse(response.location)

        if parts_response.netloc:
            self.assertEqual(response.location, expected_location, message)
        else:
            server_name = self.app.config.get('SERVER_NAME') or 'localhost'
            response_url = urljoin("http://%s" % server_name, location)
            self.assertEqual(response_url, expected_location, message)