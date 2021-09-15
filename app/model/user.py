"""
使用者相關功能
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from ..config.mysql import config as db_config
from ..model.database import Mysql


class UserModel:
    def __init__(self, user_data):
        self.username = user_data['username']
        self.password = user_data['password']
        self.role = 'admin'

    @property
    def password(self):
        raise Exception('password is not readability attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def sign_up(self):
        with Mysql(db_config) as db:
            sql = f'''
                INSERT INTO `score-analyse`.user(username, password, role)
                VALUE (%(username)s, %(password)s, %(role)s)
            '''
            bind = {
                'username': self.username,
                'password': self.password_hash,
                'role': self.role
            }
            db.exec(sql, bind)

    @classmethod
    def get_user(cls, username):
        with Mysql(db_config) as db:
            sql = f'''
                SELECT *
                FROM `score-analyse`.user
                where username=%(username)s;
            '''
            bind = {
                'username': username
            }
            results = db.query(sql, bind)
            row = next(iter(results), None)
        if row is None:
            raise Exception('01', 'username is wrong')
        cls.username = row['username']
        cls.password_hash = row['password']
        cls.role = row['role']
        return cls

    def change_password(self):
        with Mysql(db_config) as db:
            sql = f'''
                UPDATE `score-analyse`.user
                SET password=%(password)s
                WHERE username=%(username)s;
            '''
            bind = {
                'username': self.username,
                'password': self.password_hash
            }
            db.exec(sql, bind)

    def save_session(self):
        session['username'] = self.username
        session['role'] = self.role
        session.permanent = True

    @staticmethod
    def remove_session():
        session.pop('username', None)
        session.pop('role', None)
