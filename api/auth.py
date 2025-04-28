from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User  # 导入User模型类

auth_api = Blueprint('auth', __name__, template_folder='../../templates')

# 模拟用户数据库
# users = {
#     "admin": "admin123"
# }

@auth_api.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# @auth_api.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     if users.get(username) == password:
#         session['user'] = username
#         return redirect(url_for('dashboard.dashboard'))
#     else:
#         return render_template('index.html', error="用户名或密码错误")
@auth_api.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    selected_role = request.form.get('role')
    
    # 查询数据库
    user = User.query.filter_by(username=username).first()
    
    # 验证用户
    if user and user.password and user.role == selected_role: # 关键修改点
        # session['user'] = username
        session['user'] = {
            'username': username,
            'role': user.role  # 将角色存入session
        }
        return redirect(url_for('dashboard.dashboard'))
    else:
        return render_template('index.html', error="用户名或密码错误")

@auth_api.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.index'))