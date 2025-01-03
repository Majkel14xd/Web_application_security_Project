from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect('Database/database.db') 
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

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM konto WHERE login = ? AND haslo = ?', (login, haslo)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.dashboard'))  # Po udanym logowaniu przekierowanie do dashboardu
        else:
            flash('Błędny login lub hasło', 'error')

    return render_template('login.html')
