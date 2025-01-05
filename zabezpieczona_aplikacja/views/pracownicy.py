from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import sqlite3
import os
import hashlib
import re
import secrets
pracownicy_bp = Blueprint('pracownicy', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect(db_path) 
    conn.row_factory = sqlite3.Row
    return conn

# Funkcja do sanitizacji danych wejściowych
def sanitize_input(input_str):
    # Usuwamy potencjalnie niebezpieczne znaczniki HTML
    sanitized_str = re.sub(r'<.*?>', '', input_str)  # Usuwa wszystko w tagach <>
    # Usuwamy potencjalnie szkodliwe atrybuty
    sanitized_str = re.sub(r'(on\w+=["\'].*?["\'])', '', sanitized_str, flags=re.IGNORECASE)  # np. onerror, onclick
    # Usuwamy pozostałe znaki, które mogą być użyte do ataku
    sanitized_str = re.sub(r'[<>\"\'&]', '', sanitized_str)
    return sanitized_str.strip()

# Funkcja do generowania tokenu CSRF
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha256(os.urandom(64)).hexdigest()
    return session['_csrf_token']

# Funkcja do pobierania pracowników z bazy danych
def get_pracownicy(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM pracownicy"
    
    if search_query:
        sanitized_query = sanitize_input(search_query)  # Sanitizujemy dane wejściowe
        query += f" WHERE imie LIKE '%{sanitized_query}%' OR nazwisko LIKE '%{sanitized_query}%'"

    query += f" LIMIT {per_page} OFFSET {offset}"

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

# Funkcja do dodawania pracowników do bazy danych
def add_pracownik(imie, nazwisko, stanowisko):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Sanitizujemy dane wejściowe
    sanitized_imie = sanitize_input(imie)
    sanitized_nazwisko = sanitize_input(nazwisko)
    sanitized_stanowisko = sanitize_input(stanowisko)
    query = f"INSERT INTO pracownicy (imie, nazwisko, stanowisko) VALUES ('{sanitized_imie}', '{sanitized_nazwisko}', '{sanitized_stanowisko}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

# Widok dla strony pracowników
@pracownicy_bp.route('/pracownicy', methods=['GET', 'POST'])
def pracownicy():
    if 'user_id' not in session:
        return redirect(url_for('login.login')) 
    
    search_query = request.args.get('search', '')
    search_query = sanitize_input(search_query)  # Sanitizujemy dane wejściowe
    page = int(request.args.get('page', 1))
    pracownicy = get_pracownicy(search_query, per_page=8, page=page)

    if request.method == 'POST':
        # Sprawdzanie tokenu CSRF
        token = request.form.get('csrf_token')
        if not token or token != session.get('_csrf_token'):
            abort(403)  # Jeśli token jest nieprawidłowy, zwraca błąd 403

        # Sanitizujemy dane wejściowe z formularza
        imie = sanitize_input(request.form['imie'])
        nazwisko = sanitize_input(request.form['nazwisko'])
        stanowisko = sanitize_input(request.form['stanowisko'])

        add_pracownik(imie, nazwisko, stanowisko)
        session.pop('csrf_token', None)
        session['csrf_token'] = generate_csrf_token()
        return redirect(url_for('pracownicy.pracownicy', page=page, search=search_query)) 
    
    # Generowanie tokenu CSRF
    csrf_token = generate_csrf_token()

    return render_template(
        'pracownicy.html',
        pracownicy=pracownicy,
        search_query=search_query,
        page=page,
        per_page=8,
        csrf_token=csrf_token
    )
