from flask import Blueprint, request, render_template, redirect, session, jsonify, url_for

from app.models import User, House, Area, Facility, HouseImage, Order
from utils.settings import MEDIA_PATH
from utils.functions import login_required
from datetime import datetime
from sqlalchemy import and_
from flask_mail import Message
# from manage import mail
from utils import functions

import os

house_blue = Blueprint('house', __name__)


@house_blue.route('/index/')
def index():
    if request.method == 'GET':
        return render_template('index.html')


@house_blue.route('/my/', methods=['GET', 'POST'])
@login_required
def my():
    if request.method == 'GET':
        return render_template('my.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return jsonify({'code': 200, 'msg': '请求成功', 'name': user.name, 'phone': user.phone, 'avatar': user.avatar})


@house_blue.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return jsonify({'code': 200, 'msg': '请求成功', 'name': user.name})


@house_blue.route('/name/', methods=['POST'])
def name():
    if request.method == 'POST':
        user_id = session.get('user_id')
        name = request.form.get('name')
        user_name = User.query.filter(User.name == name).first()
        user = User.query.filter(User.id == user_id).first()
        if not user_name:
            user.name = name
            user.add_update()
            return jsonify({'code': 200, 'msg': '请求成功'})
        if user_name.name == user.name:
            user.name = name
            user.add_update()
            return jsonify({'code': 200, 'msg': '请求成功'})
        return jsonify({'code': 10002, 'msg': '用户名已存在'})


@house_blue.route('/avatar/', methods=['POST'])
def avatar():
    if request.method == 'POST':
        # 获取图片
        avatar = request.files.get('avatar')
        # 保存图片
        path = os.path.join(MEDIA_PATH, avatar.filename)
        avatar.save(path)
        # 修改头像
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.avatar = avatar.filename
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/logout/')
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('user.login'))


# @house_blue.route('/email_code/', methods=['POST'])
# def emailCode():
#     global email_code
#     if request.method == 'POST':
#         email = request.form.get('email')
#         msg = Message(
#             'Hello',
#             # 发件人
#             sender='1484815087@qq.com',
#             # 收件人
#             recipients=[email]
#         )
#         email_code += functions.randomCode()
#         msg.body = email_code
#         # msg.html = '<b>testing</b>'
#         mail.send(msg)
#         return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/auth/', methods=['GET', 'POST'])
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    if request.method == 'POST':
        code = request.form.get('code')
        if code == 'sxr_code':
            user_id = session.get('user_id')
            id_name = request.form.get('id_name')
            id_card = request.form.get('id_card')
            user = User.query.filter(User.id == user_id).first()
            if id_name != '' and id_card != '':
                user.id_name = id_name
                user.id_card = id_card
                user.add_update()
                return jsonify({'code': 200, 'msg': '请求成功'})
            return jsonify({'code': 10000, 'msg': '信息有误'})
        return jsonify({'code': 1000, 'msg': '验证码错误'})


@house_blue.route('/auth_all/')
def auth_all():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return jsonify({'code': 200, 'msg': '请求成功', 'id_name': user.id_name, 'id_card': user.id_card})


@house_blue.route('/my_house/', methods=['GET', 'POST'])
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        house = House.query.order_by('-id')[0:3]
        user = User.query.filter(User.id == user_id).first()
        houses = []
        for hou in house:
            houses.append(hou.to_dict())
        if user:
            name = user.name
        else:
            name = ''
        return jsonify({'code': 200, 'msg': '请求成功', 'house': houses, 'user_id': user_id, 'name': name})


@house_blue.route('/myhouse/', methods=['POST'])
def myhouse():
    if request.method == 'POST':
        user_id = session.get('user_id')
        house = House.query.filter(House.user_id == user_id)
        houses = []
        for hou in house:
            houses.append(hou.to_dict())
        return jsonify({'code': 200, 'msg': '请求成功', 'house': houses})


@house_blue.route('/new_house/', methods=['GET', 'PATCH'])
@login_required
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'PATCH':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        area_id = request.form.get('area_id')
        area = Area.query.filter(Area.id == area_id).first()
        title = request.form.get('title')
        price = request.form.get('price')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facility = request.form.get('facility')
        f_n = facility.split(',')
        house = House()
        house.user_id = user.id
        house.area_id = area.id
        house.title = title
        house.price = price
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        for i in f_n:
            if i == '':
                break
            house.facilities.append(Facility.query.get(int(i)))
        house.add_update()
        session['house_id'] = house.id
        return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/area/')
def area():
    if request.method == 'GET':
        areas = Area.query.all()
        are = []
        for area in areas:
            are.append(area.to_dict())
        return jsonify({'code': 200, 'msg': '请求成功', 'area': are})


@house_blue.route('/facility/', methods=['GET', 'PATCH'])
def facility():
    if request.method == 'GET':
        facility = Facility.query.all()
        facilitys = []
        for facility_ in facility:
            facilitys.append(facility_.to_dict())
        return jsonify({'code': 200, 'msg': '请求成功', 'facility': facilitys})
    if request.method == 'PATCH':
        house_img = request.files.get('house_image')
        if house_img:
            path = os.path.join(MEDIA_PATH, house_img.filename)
            house_img.save(path)
            houseImg = HouseImage()
            house_id = session.get('house_id')
            house = House.query.filter(House.id == house_id).first()
            houseImg.house_id = house_id
            houseImg.url = house_img.filename
            houseImg.add_update()
            house.index_image_url = house_img.filename
            house.add_update()
            return jsonify({'code': 200, 'msg': '请求成功', 'img': house_img.filename})
        return jsonify({'code': 1000, 'msg': '请求成功'})


@house_blue.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':

        return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/my_search/')
def my_search():
    if request.method == 'GET':
        area_id = int(request.args.get('aid'))
        sd = datetime.strptime(request.args.get('sd'), '%Y-%m-%d')
        ed = datetime.strptime(request.args.get('ed'), '%Y-%m-%d')
        houses = []
        avatar = []
        # 订单入住时间大于搜索开始时间，离开时间小于搜索离开时间
        order1 = Order.query.filter(and_(Order.begin_date >= sd, Order.end_date <= ed)).all()
        # 订单入住时间小于搜索开始时间，离开时间大于搜索离开时间
        order2 = Order.query.filter(and_(Order.begin_date <= sd, Order.end_date >= ed)).all()
        # 订单入住时间小于搜索开始时间，离开时间小于搜索离开时间
        order3 = Order.query.filter(and_(Order.begin_date <= sd, Order.end_date >= sd)).all()
        # 订单入住时间大于搜索开始时间，离开时间大于搜索离开时间
        order4 = Order.query.filter(and_(Order.begin_date <= ed, Order.end_date >= ed)).all()
        order = list(set(order1 + order2 + order3 + order4))
        house_id = []
        content = request.args.get('content')
        if content == '最新上线':
            house = House.query.filter(House.area_id == area_id).order_by('-id')
        if content == '价格 低-高':
            house = House.query.filter(House.area_id == area_id).order_by('price')
        if content == '价格 高-低':
            house = House.query.filter(House.area_id == area_id).order_by('-price')
        for ord in order:
            house_id.append(ord.house_id)
        for hou in house:
            if hou.id not in house_id:
                avatar.append(hou.user.avatar)
                houses.append(hou.to_dict())
        if houses:
            return jsonify({'code': 200, 'msg': '请求成功', 'house': houses, 'avatar': avatar})
        return jsonify({'code': 10000, 'msg': '请求成功'})


@house_blue.route('/detail/')
def detail():
    if request.method == 'GET':
        return render_template('detail.html')


@house_blue.route('/detail/<int:id>/', methods=['GET'])
def detail_house(id):
    if request.method == 'GET':
        house_id = int(id)
        house = House.query.filter(House.id == id).first()
        house_user_id = house.user_id
        user_house = User.query.filter(User.id == house_user_id).first()
        reserve = 0
        user_id = session.get('user_id')
        if user_id:
            if user_id == house_user_id:
                reserve = 1
        return jsonify(
            {'code': 200, 'msg': '请求成功', 'user_house': user_house.to_basic_dict(), 'house_detail': house.to_full_dict(), 'reserve': reserve})
