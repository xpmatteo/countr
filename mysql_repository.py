
import os
import pymysql

class MysqlCountRepository:
    def __init__(self, thread_locals):
        self.thread_locals = thread_locals

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
        connection = getattr(self.thread_locals, '_connection', None)
        if connection is None:
            connection = self.thread_locals._connection = pymysql.connect(
                db=os.environ['RDS_DB_NAME'],
                port=int(os.environ['RDS_PORT']),
                host=os.environ['RDS_HOSTNAME'],
                user=os.environ['RDS_USERNAME'],
                password=os.environ['RDS_PASSWORD'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
                )
        return self.thread_locals._connection.cursor()

