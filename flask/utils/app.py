from utils.settings import STATIC_PATH, TEMPLATE_PATH
from flask import Flask
from utils.config import Conf
from app.models import db
from app.user_views import user_blue
from app.house_views import house_blue
from app.orders_views import orders_blue
# from app.mail_view import mail_blue


def create_app():
    app = Flask(__name__,
                static_folder=STATIC_PATH,
                template_folder=TEMPLATE_PATH
                )

    # 加载配置
    app.config.from_object(Conf)

    # 注册蓝图
    app.register_blueprint(blueprint=user_blue, url_prefix='/user')
    app.register_blueprint(blueprint=house_blue, url_prefix='/house')
    app.register_blueprint(blueprint=orders_blue, url_prefix='/orders')
    # app.register_blueprint(blueprint=mail_blue, url_prefix='/mail')

    # 初始化
    db.init_app(app)
    return app
