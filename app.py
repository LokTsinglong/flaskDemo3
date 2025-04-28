from flask import Flask, render_template
from api.auth import auth_api
from api.dashboard import dashboard_api
from api.workspace import workspace_api 
from flask_migrate import Migrate

app = Flask(__name__,static_folder="static")

# @app.route("/")
# def index():
#    return render_template("index.html")

# if __name__ == '__main__':
#    app.run(debug = True)

# #函数工厂
# def create_app():
#     app = Flask(__name__, static_folder="static")
#     app.secret_key = 'your_secure_secret_key_here'  # 生产环境请使用随机生成
    
#     # 注册蓝图
#     app.register_blueprint(auth_api)
#     app.register_blueprint(dashboard_api)
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)

app.secret_key = 'your_secret_key' 
app.register_blueprint(auth_api) 
app.register_blueprint(dashboard_api)
app.register_blueprint(workspace_api)

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask_app_3'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)

from models import db

db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)

