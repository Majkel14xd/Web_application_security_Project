from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect(db_path) 
    conn.row_factory = sqlite3.Row
    return conn

# Strona logowania
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))  #

    if request.method == 'POST':
        login = request.form['login']
        haslo = request.form['haslo']

        query = f"SELECT * FROM konto WHERE login = '{login}' AND haslo = '{haslo}'"
        conn = get_db_connection()
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.dashboard'))  # Po udanym logowaniu przekierowanie do dashboardu
        else:
            flash('Błędny login lub hasło', 'error')

    return render_template('login.html')
