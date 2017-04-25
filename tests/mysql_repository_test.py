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
        result = self._do_getitem(key)
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
        return self._do_getitem(key)

    def __iter__(self):
        cursor = self._get_cursor()
        cursor.execute('select * from counts')
        rows = cursor.fetchall()
        for row in rows:
            yield row['id']

    def _do_getitem(self, key):
        cursor = self._get_cursor()
        cursor.execute('select value from counts where id = %s', (key))
        return cursor.fetchone()

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

    def close(self):
        self._cursor.close()
        self._cursor = None


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
        self.assertEqual(set(['9','11','123']), set([x for x in self.repository]))


if __name__ == '__main__':
    unittest.main()
