from flask import Blueprint, request, render_template, redirect, jsonify, session

from app.models import User
from utils.functions import randomCode

user_blue = Blueprint('user', __name__)


@user_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        if not all([phone, password]):
            return jsonify({'code': 10001, 'msg': '请填写完整的信息'})
        user = User.query.filter(User.phone == phone).first()
        if not user or not user.check_pwd(pwd=password):
            return jsonify({'code': 10000, 'msg': '用户名或密码错误'})
        session['user_id'] = user.id
        return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user1 = User.query.filter(User.phone == phone).first()
        if not user1:
            if password == password2:
                user = User()
                user.phone = phone
                user.email = email
                user.password = password
                user.add_update()
                return jsonify({'code': 200, 'msg': '注册成功'})
            else:
                return jsonify({'code': 10003, 'msg': '密码不一致'})
        else:
            return jsonify({'code': 10002, 'msg': '手机号已存在'})


@user_blue.route('/code/', methods=['GET'])
def code():
    if request.method == 'GET':
        code = randomCode()
        return jsonify({'code': code})
