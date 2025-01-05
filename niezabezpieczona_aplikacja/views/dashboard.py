from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@dashboard_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login.login')) 

    user_id = session['user_id']
    
    conn = get_db_connection()
    query = f"SELECT login FROM konto WHERE id = {user_id}"
    user = conn.execute(query).fetchone()    
    conn.close()

    if user:
        welcome_message = f"Witaj, {user['login']}!"
    else:
        welcome_message = "Nie znaleziono użytkownika."

    return render_template('dashboard.html', welcome_message=welcome_message)
