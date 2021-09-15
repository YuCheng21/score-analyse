from . import app
from flask import redirect, url_for, abort, flash, request, session

from mysql.connector import errorcode

from ...model.user import UserModel


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        abort(404)
    elif request.method == 'POST':
        try:
            user_data = request.values.to_dict()
            if '' in list(user_data.values()):
                raise Exception('00', 'user_data can not be empty string')
            new_user = UserModel(user_data)
            new_user.sign_up()
        except Exception as e:
            if e.args[0] == errorcode.ER_DUP_ENTRY:
                flash('重複的帳號', 'error')
                return redirect(url_for('root.index'))
            elif e.args[0] == '00':
                flash('帳號與密碼禁止為空', 'error')
                return redirect(url_for('root.index'))
            print(e)
            abort(404)
        else:
            flash('註冊成功！', category='success-toast')
            return redirect(url_for('root.index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        abort(404)
    elif request.method == 'POST':
        try:
            user_data = request.values.to_dict()
            user_info = UserModel.get_user(user_data['username'])
            # something weird
            if not user_info.verify_password(user_info, user_data['password']):
                flash('密碼錯誤', 'error')
                return redirect(url_for('root.index'))
        except Exception as e:
            if e.args[0] == '01':
                flash('帳號錯誤', 'error')
                return redirect(url_for('root.index'))
            print(e)
            abort(404)
        else:
            user_info.save_session(user_info)
            flash('登入成功！', category='success-toast')
            return redirect(url_for('root.index'))


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        abort(404)
    elif request.method == 'POST':
        form_data = request.values.to_dict()
        user_info = UserModel({
            'username': session['username'],
            'password': form_data['password']
        })
        try:
            user_info.change_password()
        except Exception as e:
            print(e)
            abort(404)
        else:
            flash('修改成功', category='success')
            return redirect(url_for('root.index'))


@app.route('/logout')
def logout():
    UserModel.remove_session()
    flash('登出成功！', category='success-toast')
    return redirect(url_for('root.index'))
