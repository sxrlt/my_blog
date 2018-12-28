import random
from functools import wraps
from flask import session, url_for, redirect


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            session['user_id']
        except:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return inner


def get_sqlalchemy_uri(DATABASE):
    # mysql+pymysql://root:123456@127.0.0.1:3306/flask
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']

    return '%s+%s://%s:%s@%s:%s/%s' % (engine, driver, user, password, host, port, name)


def randomCode():
    code = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    randomCode = ''
    for i in range(4):
        n = random.randint(0, len(code) - 1)
        randomCode += str(code[n])
    return randomCode