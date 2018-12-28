
from flask import Blueprint, request, jsonify
from flask_mail import Message
from manage import mail

mail_blue = Blueprint('email', __name__)


@mail_blue.route('/index/')
def index():
    if request.method == 'GET':
        return 'ok'


@mail_blue.route('/email_code/', methods=['POST'])
def emailCode():
    if request.method == 'POST':
        email = request.form.get('email')
        msg = Message(
            'Hello',
            # 发件人
            sender='1484815087@qq.com',
            # 收件人
            recipients=[email]
        )
        msg.body = 'sxr_code'
        # msg.html = '<b>testing</b>'
        mail.send(msg)
        return jsonify({'code': 200, 'msg': '请求成功'})
