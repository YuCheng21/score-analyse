"""
資料庫連接功能。
"""
import mysql.connector


class Mysql:
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor(dictionary=True)

    def exec(self, sql, params=()):
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def query(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
