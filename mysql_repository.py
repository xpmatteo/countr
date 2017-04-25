
import os
import pymysql
from flask import g

class MysqlCountRepository:
    def __getitem__(self, key):
        result = self._do_getitem(key)
        if not result:
            raise KeyError
        return result['value']

    def __setitem__(self, key, value):
        with self._get_cursor() as cursor:
            if key in self:
                cursor.execute('update counts set value = %s where id = %s', (value, key))
            else:
                cursor.execute('insert into counts (id, value) values (%s,%s)', (key, value))

    def __contains__(self, key):
        return self._do_getitem(key)

    def __iter__(self):
        with self._get_cursor() as cursor:
            cursor.execute('select * from counts')
            rows = cursor.fetchall()
            for row in rows:
                yield row['id']

    def _do_getitem(self, key):
        with self._get_cursor() as cursor:
            cursor.execute('select value from counts where id = %s', (key))
            return cursor.fetchone()

    def _get_cursor(self):
        connection = getattr(g, '_connection', None)
        if connection is None:
            connection = g._connection = pymysql.connect(
                db=os.environ['MYSQL_DATABASE_DB'],
                host=os.environ['MYSQL_DATABASE_HOST'],
                user=os.environ['MYSQL_DATABASE_USER'],
                password=os.environ['MYSQL_DATABASE_PASSWORD'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
                )
        return g._connection.cursor()

