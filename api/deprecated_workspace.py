from flask import Blueprint, render_template, session, redirect, url_for

workspace_api = Blueprint('workspace', __name__, template_folder='../../templates')
@workspace_api.route('/workspace1')
def workspace1():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace1.html")

@workspace_api.route('/workspace2')
def workspace2():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace2.html")

@workspace_api.route('/workspace3')
def workspace3():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace3.html")