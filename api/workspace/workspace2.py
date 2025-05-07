from flask import Blueprint, render_template, session, redirect, url_for,jsonify,request

# 注册蓝图
workspace2_api = Blueprint('workspace2_api', __name__, template_folder='../../templates')

@workspace2_api.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace2.html")
