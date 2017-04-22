#!/usr/local/bin/python3

import os
import unittest

from context import countr

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.app = countr.app.test_client()

    def test_get_root(self):
        response = self.app.get('/')
        assert b'No counters defined' in response.data

if __name__ == '__main__':
    unittest.main()
