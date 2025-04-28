from flask import Blueprint, render_template, session, redirect, url_for

dashboard_api = Blueprint('dashboard', __name__, template_folder='../../templates')

@dashboard_api.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.index'))
    return render_template("dashboard.html", username=session['user']['username'])  