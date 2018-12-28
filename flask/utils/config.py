
from utils.functions import get_sqlalchemy_uri
from utils.settings import DATABASE


class Conf():
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri(DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = '1212'
    # 设置qq邮箱服务器地址
    MAIL_SERVER = 'smtp.qq.com'
    # 设置是否启用传输层安全协议
    MAIL_USE_TLS = True
    # 设置传输邮箱地址
    MAIL_USERNAME = '1484815087@qq.com'
    # qq邮箱输入授权码
    MAIL_PASSWORD = 'zfridjzksqfygaci'
