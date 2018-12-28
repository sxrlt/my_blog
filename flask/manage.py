
from flask_script import Manager

from utils.app import create_app
from flask_mail import Mail


# 获取flask对象app
app = create_app()

mail = Mail(app)

# 管理app
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
