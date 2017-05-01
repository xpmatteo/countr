#!/usr/local/bin/python3

import os
import unittest
import context
import pymysql
from mysql_repository import MysqlCountRepository

class FakeAppGlobals:
    pass

class MysqlRepositoryTest(unittest.TestCase):

    def setUp(self):
        os.environ['RDS_DB_NAME'] = 'countr_test'
        os.environ['RDS_HOSTNAME'] = 'localhost'
        os.environ['RDS_PORT'] = '3306'
        os.environ['RDS_USERNAME'] = 'countr'
        os.environ['RDS_PASSWORD'] = 'countr'

        connection = pymysql.connect(
            db=os.environ['RDS_DB_NAME'],
            host=os.environ['RDS_HOSTNAME'],
            user=os.environ['RDS_USERNAME'],
            password=os.environ['RDS_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
            )
        cursor =connection.cursor()

        cursor.execute('SET sql_notes = 0')
        with open('sql/001_create_counts.sql', 'r') as sql_file:
            cursor.execute(sql_file.read());
        cursor.execute('SET sql_notes = 1')

        cursor.execute('truncate table counts')
        connection.close()

        self.repository = MysqlCountRepository(FakeAppGlobals())

    def test_read_one_counter(self):
        self.repository['123'] = 999
        self.assertEqual(999, self.repository['123'])

    def test_count_exists_test(self):
        self.repository['123'] = 999
        self.assertTrue('123' in self.repository)
        self.assertFalse('222' in self.repository)

    def test_non_existent_counter(self):
        with self.assertRaises(KeyError):
            self.repository['2222']

    def test_create_counter(self):
        self.repository['111'] = 222
        self.assertTrue('111' in self.repository)
        self.assertEqual(222, self.repository['111'])

    def test_update_counter(self):
        self.repository['9'] = 10
        self.repository['9'] = 11
        self.assertEqual(11, self.repository['9'])

    def test_iterate(self):
        self.repository['9'] = 10
        self.repository['11'] = 12
        self.assertEqual(set(['9','11']), set([x for x in self.repository]))

    def test_connection_is_committed(self):
        self.repository['pippo'] = 10
        other_repo = MysqlCountRepository(FakeAppGlobals())
        self.assertEqual(10, other_repo['pippo'])


if __name__ == '__main__':
    unittest.main()
