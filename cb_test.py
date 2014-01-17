# -*- coding: utf-8 -*-
"""
Flaskr Tests

Crawler Benchmark tests.
"""
import os
import cb
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):


    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, cb.app.config['DATABASE'] = tempfile.mkstemp()
        cb.app.config['TESTING'] = True
        self.app = cb.app.test_client()
        cb.init_db()


    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(cb.app.config['DATABASE'])


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # testing functions


    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data


    def test_login_logout(self):
        """Make sure login and logout works"""
        rv = self.login(cb.app.config['USERNAME'],
                        cb.app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(cb.app.config['USERNAME'] + 'x',
                        cb.app.config['PASSWORD'])
        assert b'Invalid username' in rv.data
        rv = self.login(cb.app.config['USERNAME'],
                        cb.app.config['PASSWORD'] + 'x')
        assert b'Invalid password' in rv.data


    def test_messages(self):
        """Test that messages work"""
        self.login(cb.app.config['USERNAME'],
                   cb.app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
