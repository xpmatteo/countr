#!/usr/local/bin/python3

import os
import unittest
import context
import countr
import pymysql

class MysqlRepositoryTest(unittest.TestCase):

    def setUp(self):
        os.environ['MYSQL_DATABASE_DB'] = 'countr_test'
        os.environ['MYSQL_DATABASE_HOST'] = 'localhost'
        os.environ['MYSQL_DATABASE_USER'] = 'countr'
        os.environ['MYSQL_DATABASE_PASSWORD'] = 'countr'
        # self.repository = MysqlCountRepository()


    def test_connect(self):
        pymysql.connect(
            db=os.environ['MYSQL_DATABASE_DB'],
            host=os.environ['MYSQL_DATABASE_HOST'],
            user=os.environ['MYSQL_DATABASE_USER'],
            password=os.environ['MYSQL_DATABASE_PASSWORD']
            )
        pass



if __name__ == '__main__':
    unittest.main()
