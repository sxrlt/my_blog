from flask import Blueprint, request, render_template, redirect, session, jsonify, url_for
from utils.functions import login_required
from app.models import House, Order
from datetime import datetime
from utils.functions import randomCode


orders_blue = Blueprint('orders', __name__)


@orders_blue.route('/my_order/', methods=['GET', 'POST'])
def my_order():
    if request.method == 'GET':
        return render_template('orders.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        order = Order.query.filter(Order.user_id == user_id)
        orders = []
        ord_id = []
        if order:
            for ord in order:
                ord_id.append(str(ord.id) + randomCode())
                orders.append(ord.to_dict())
            return jsonify({'code': 200, 'msg': '请求成功', 'order': orders, 'ord_id': ord_id})
        return jsonify({'code': 10000, 'msg': '请求成功'})


@orders_blue.route('/comment/', methods=['POST'])
def comment():
    if request.method == 'POST':
        comment = request.form.get('comments')
        order_id = int(request.form.get('order_id'))
        order = Order.query.filter(Order.id == order_id).first()
        order.comment = comment
        order.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})


@orders_blue.route('/booking/', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'GET':
        return render_template('booking.html')
    if request.method == 'POST':
        house_id = int(request.form.get('house_id'))
        house = House.query.filter(House.id == house_id).first()
        days = request.form.get('days')
        max_days = house.max_days
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        amount = request.form.get('amount')
        user_id = session.get('user_id')
        order = Order()
        if house.max_days == 0 or days <= max_days:
            order.days = days
            order.house_id = house_id
            order.user_id = user_id
            order.begin_date = begin_date
            order.end_date = end_date
            order.house_price = house.price
            order.amount = amount
            order.add_update()
            return jsonify({'code': 200, 'msg': '请求成功'})
        return jsonify({'code': 10000, 'msg': '请求成功'})


@orders_blue.route('/booking/<int:id>/')
def booking_house(id):
    if request.method == 'GET':
        house_id = int(id)
        house = House.query.filter(House.id == house_id).first()
        return jsonify({'code': 200, 'msg': '请求成功', 'house': house.to_dict()})


@orders_blue.route('/lorders/', methods=['GET', 'POST'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        house = House.query.filter(House.user_id == user_id)
        house_id = []
        for i in house:
            house_id.append(i.id)
        order = Order.query.all()
        lorder = []
        for i in order:
            if i.house_id in house_id:
                lorder.append(i.to_dict())
        if lorder == []:
            return jsonify({'code': 10000, 'msg': '请求成功'})
        return jsonify({'code': 200, 'msg': '请求成功', 'lorder': lorder})
