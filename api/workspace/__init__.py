from flask import Blueprint,session,redirect,url_for,render_template


workspace_main = Blueprint('workspace_main', __name__)

# 这边路由一定要改下，否则会跳到index.html也就是登录的那个界面
@workspace_main.route('/workspace_main')
def index():
    if 'user' not in session:
        
        return redirect(url_for('auth.login'))
    return render_template("dashboard.html")

#延迟导入，否则可能会有(most likely due to a circular import
from .workspace1 import workspace1_api
workspace_main.register_blueprint(workspace1_api, url_prefix='/workspace1')