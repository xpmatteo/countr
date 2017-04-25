#!/usr/local/bin/python3

import os
import unittest
import context
import countr
import pymysql

class MysqlCountRepository:
    def __getitem__(self, key):
        self.connection = pymysql.connect(
            db=os.environ['MYSQL_DATABASE_DB'],
            host=os.environ['MYSQL_DATABASE_HOST'],
            user=os.environ['MYSQL_DATABASE_USER'],
            password=os.environ['MYSQL_DATABASE_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
            )
        self.cursor = self.connection.cursor()
        self.cursor.execute('select value from counts where id = %s', (key))
        return self.cursor.fetchone()['value']

class MysqlRepositoryTest(unittest.TestCase):

    def setUp(self):
        os.environ['MYSQL_DATABASE_DB'] = 'countr_test'
        os.environ['MYSQL_DATABASE_HOST'] = 'localhost'
        os.environ['MYSQL_DATABASE_USER'] = 'countr'
        os.environ['MYSQL_DATABASE_PASSWORD'] = 'countr'

        self.connection = pymysql.connect(
            db=os.environ['MYSQL_DATABASE_DB'],
            host=os.environ['MYSQL_DATABASE_HOST'],
            user=os.environ['MYSQL_DATABASE_USER'],
            password=os.environ['MYSQL_DATABASE_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
            )
        self.cursor = self.connection.cursor()
        self.cursor.execute('truncate table counts')
        self.connection.commit()
        self.repository = MysqlCountRepository()

    def tearDown(self):
        self.connection.close()

    def test_connect(self):
        sql = 'select 3 + 4 as sum'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.assertEqual(7, result['sum'])

        sql = "select concat(%s, %s, %s) as concatenation"
        self.cursor.execute(sql, ('Dear ', 'Mr. ', "O'Malley"))
        result = self.cursor.fetchone()
        self.assertEqual("Dear Mr. O'Malley", result['concatenation'])

    def test_read_one_counter(self):
        self.cursor.execute("insert into counts (id, value) values ('123', 999)")
        self.connection.commit()
        self.assertEqual(999, self.repository['123'])

    def xtest_non_existent_counter(self):
        with self.assertRaises(KeyError) as context:
            self.repository['456']


if __name__ == '__main__':
    unittest.main()
