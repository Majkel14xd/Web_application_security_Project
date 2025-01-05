from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
import sqlite3
import os
import hashlib
import re

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Funkcja do generowania tokenu CSRF
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha256(os.urandom(64)).hexdigest()
    return session['_csrf_token']

def sanitize_input(input_str):

    # Usuwamy potencjalnie niebezpieczne znaczniki HTML
    sanitized_str = re.sub(r'<.*?>', '', input_str)  # Usuwa wszystko w tagach <>

    # Usuwamy potencjalnie szkodliwe atrybuty
    sanitized_str = re.sub(r'(on\w+=["\'].*?["\'])', '', sanitized_str, flags=re.IGNORECASE)  # np. onerror, onclick

    # Usuwamy pozostałe znaki, które mogą być użyte do ataku
    sanitized_str = re.sub(r'[<>\"\'&]', '', sanitized_str)

    return sanitized_str.strip()

# Strona logowania
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))  # Jeśli użytkownik jest zalogowany, przekierowanie do dashboardu
    csrf_token = generate_csrf_token()
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('_csrf_token'):
            abort(403)  # Zwraca błąd 403, jeśli token jest nieprawidłowy

        # Pobranie danych i ich sanitizacja
        login = sanitize_input(request.form['login'])
        haslo = sanitize_input(request.form['haslo'])

        query = f"SELECT * FROM konto WHERE login = '{login}' AND haslo = '{haslo}'"
        conn = get_db_connection()
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.dashboard'))  # Po udanym logowaniu przekierowanie do dashboardu
        else:
            flash('Błędny login lub hasło', 'error')

    # Generowanie tokenu CSRF
  
    session.pop('csrf_token', None)
    return render_template('login.html', csrf_token=csrf_token)
