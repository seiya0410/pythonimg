from flask import Flask, session, redirect
from functools import wraps


USER_LOGIN_LIST = {
    'taro': 'aaa',
    'jiro': 'bbb',
    'sabu': 'ccc'
}

def is_login():
    return 'login' in session

def try_login(form):
    user = form.get('user', '')
    password = form.get('pw', '')

    if user not in USER_LOGIN_LIST: return False
    if USER_LOGIN_LIST[user] != password: return False

    session['login'] = user
    return True

def get_id():
    return session['login'] if is_login() else 'not login'


def get_allusers():
    return [u for u in USER_LOGIN_LIST]

def try_logout():
    session.pop('login', None)
    return True

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        if not is_login():
            return redirect('/login')
        return func(*args, **kargs)
    return wrapper