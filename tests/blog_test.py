#!/usr/local/bin/python3

import os
import unittest
import context
import countr

class BlogTest(unittest.TestCase):

    def setUp(self):
        countr.counts = {}
        countr.app.config['TESTING'] = True
        self.app = countr.app.test_client()

    def test_get_root(self):
        response = self.app.get('/')
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/counts/', response.headers['location'])

    def test_create_count(self):
        countr.random.seed(1)
        response = self.app.post('/counts/')
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/counts/144272509', response.headers['location'])
        self.assertEqual(0, countr.counts['144272509'])

    def test_get_nonexistent_count(self):
        response = self.app.get('/counts/12345')
        self.assertEqual(404, response.status_code)

    def test_get_count(self):
        countr.counts['1234'] = 9
        response = self.app.get('/counts/1234')
        self.assertEqual(200, response.status_code)
        self.assertEqual('text/plain', response.content_type)
        self.assertEqual(b'9', response.data)

    def test_increment_count(self):
        countr.counts['1234'] = 4
        response = self.app.post('/counts/1234', data=dict(increment=3))
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/counts/1234', response.headers['location'])
        self.assertEqual(7, countr.counts['1234'])


if __name__ == '__main__':
    unittest.main()
