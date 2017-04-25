#!/usr/local/bin/python3

import os
import unittest
import context
import countr
import pymysql

class MysqlCountRepository:
    def __init__(self):
        self._cursor = None

    def __getitem__(self, key):
        cursor = self._get_cursor()
        cursor.execute('select value from counts where id = %s', (key))
        result = cursor.fetchone()
        if not result:
            raise KeyError
        return result['value']

    def __setitem__(self, key, value):
        cursor = self._get_cursor()
        if key in self:
            cursor.execute('update counts set value = %s where id = %s', (value, key))
        else:
            cursor.execute('insert into counts (id, value) values (%s,%s)', (key, value))

    def __contains__(self, key):
        cursor = self._get_cursor()
        cursor.execute('select value from counts where id = %s', (key))
        result = cursor.fetchone()
        return result

    def _get_cursor(self):
        if not self._cursor:
            connection = pymysql.connect(
                db=os.environ['MYSQL_DATABASE_DB'],
                host=os.environ['MYSQL_DATABASE_HOST'],
                user=os.environ['MYSQL_DATABASE_USER'],
                password=os.environ['MYSQL_DATABASE_PASSWORD'],
                cursorclass=pymysql.cursors.DictCursor
                )
            self._cursor = connection.cursor()
        return self._cursor


class MysqlRepositoryTest(unittest.TestCase):

    def setUp(self):
        os.environ['MYSQL_DATABASE_DB'] = 'countr_test'
        os.environ['MYSQL_DATABASE_HOST'] = 'localhost'
        os.environ['MYSQL_DATABASE_USER'] = 'countr'
        os.environ['MYSQL_DATABASE_PASSWORD'] = 'countr'

        connection = pymysql.connect(
            db=os.environ['MYSQL_DATABASE_DB'],
            host=os.environ['MYSQL_DATABASE_HOST'],
            user=os.environ['MYSQL_DATABASE_USER'],
            password=os.environ['MYSQL_DATABASE_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
            )
        cursor =connection.cursor()
        cursor.execute('truncate table counts')
        cursor.execute("insert into counts (id, value) values ('123', 999)")
        connection.commit()
        connection.close()

        self.repository = MysqlCountRepository()

    def test_read_one_counter(self):
        self.assertEqual(999, self.repository['123'])
        self.assertTrue(999, self.repository['123'])

    def test_count_exists_test(self):
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


if __name__ == '__main__':
    unittest.main()
