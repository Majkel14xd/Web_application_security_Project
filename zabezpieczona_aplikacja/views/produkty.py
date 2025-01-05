from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os
import secrets
import re

produkty_bp = Blueprint('produkty', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect(db_path) 
    conn.row_factory = sqlite3.Row
    return conn

# Funkcja do generowania tokenu CSRF
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)  # Generowanie losowego tokenu CSRF
    return session['csrf_token']

# Funkcja do sanitizacji danych wejściowych
def sanitize_input(input_str):
    sanitized_str = re.sub(r'<.*?>', '', input_str)  # Usuwa znaczniki HTML
    sanitized_str = re.sub(r'(on\w+=["\'].*?["\'])', '', sanitized_str, flags=re.IGNORECASE)  # Usuwa zdarzenia onerror, onclick
    sanitized_str = re.sub(r'[<>\"\'&]', '', sanitized_str)  # Usuwa pozostałe niebezpieczne znaki
    return sanitized_str.strip()

# Funkcja do pobierania produktów z bazy danych
def get_produkty(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM produkty"
    if search_query:
        sanitized_query = sanitize_input(search_query)  # Sanitizacja danych wejściowych
        query += f" WHERE nazwa LIKE '%{sanitized_query}%'"

    query += f" LIMIT {per_page} OFFSET {offset}"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

# Funkcja do dodawania produktu do bazy danych
def add_produkt(nazwa, cena):
    conn = get_db_connection()
    cursor = conn.cursor()
    sanitized_nazwa = sanitize_input(nazwa)  # Sanitizacja danych wejściowych
    query = f"INSERT INTO produkty (nazwa, cena) VALUES ('{sanitized_nazwa}', {cena})"
    cursor.execute(query)
    conn.commit()
    conn.close()

# Widok dla strony produktów
@produkty_bp.route('/produkty', methods=['GET', 'POST'])
def produkty():
    if 'user_id' not in session:
        return redirect(url_for('login.login')) 
    
    search_query = request.args.get('search', '')
    search_query = sanitize_input(search_query)  # Sanitizacja danych wejściowych
    page = int(request.args.get('page', 1))
    produkty = get_produkty(search_query, per_page=8, page=page)

    # Generowanie tokenu CSRF
    csrf_token = generate_csrf_token()

    if request.method == 'POST':
        # Sprawdzenie poprawności tokenu CSRF
        token_from_form = request.form.get('csrf_token')
        if token_from_form != session.get('csrf_token'):
            return "CSRF token invalid", 400  # Można dodać lepszą obsługę błędów
        
        nazwa = sanitize_input(request.form['nazwa'])  # Sanitizacja danych wejściowych
        try:
            cena = float(request.form['cena'])  # Walidacja typu danych
        except ValueError:
            return "Invalid price format", 400  # Obsługa błędu dla nieprawidłowego formatu ceny
        
        add_produkt(nazwa, cena)
        session.pop('csrf_token', None)
        session['csrf_token'] = generate_csrf_token()


        return redirect(url_for('produkty.produkty', page=page, search=search_query))

    return render_template(
        'produkty.html',
        produkty=produkty,
        search_query=search_query,
        page=page,
        per_page=8,
        csrf_token=csrf_token  # Przekazanie tokenu CSRF do szablonu
    )
