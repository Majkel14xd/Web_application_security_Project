from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os
import secrets
import re

sprzedaz_bp = Blueprint('sprzedaz', __name__, template_folder='templates', static_folder='static')
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

# Funkcja do pobierania sprzedaży
def get_sprzedaz(per_page=8, page=1, start_date=None, end_date=None):
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT sprzedaz.id, pracownicy.imie || ' ' || pracownicy.nazwisko AS pracownik,
               produkty.nazwa AS produkt, sprzedaz.data_sprzedazy
        FROM sprzedaz
        JOIN pracownicy ON sprzedaz.id_pracownika = pracownicy.id
        JOIN produkty ON sprzedaz.id_produktu = produkty.id
    """

    if start_date and end_date:
        sanitized_start_date = sanitize_input(start_date)  # Sanitizacja daty początkowej
        sanitized_end_date = sanitize_input(end_date)  # Sanitizacja daty końcowej
        query += f" WHERE sprzedaz.data_sprzedazy BETWEEN '{sanitized_start_date}' AND '{sanitized_end_date}'"

    query += f" LIMIT {per_page} OFFSET {offset}"

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

# Funkcja do pobierania listy produktów
def get_produkty():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nazwa FROM produkty")
    produkty = cursor.fetchall()
    conn.close()
    return produkty

# Funkcja do pobierania listy pracowników o stanowisku "Sklepowa"
def get_sklepowi_pracownicy():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, imie || ' ' || nazwisko AS pelne_imie FROM pracownicy WHERE stanowisko = 'Sklepowa'")
    pracownicy = cursor.fetchall()
    conn.close()
    return pracownicy

# Funkcja do dodawania sprzedaży
def add_sprzedaz(id_pracownika, id_produktu, data_sprzedazy):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO sprzedaz (id_pracownika, id_produktu, data_sprzedazy) VALUES ({id_pracownika}, {id_produktu}, '{data_sprzedazy}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

# Widok dla strony sprzedaży
@sprzedaz_bp.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if 'user_id' not in session:
        return redirect(url_for('login.login')) 
    
    page = int(request.args.get('page', 1))
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    # Jeśli daty są podane, przekazujemy je do funkcji get_sprzedaz
    sprzedaz = get_sprzedaz(per_page=8, page=page, start_date=start_date, end_date=end_date)

    # Generowanie tokenu CSRF
    csrf_token = generate_csrf_token()

    if request.method == 'POST':
        # Sprawdzenie poprawności tokenu CSRF
        token_from_form = request.form.get('csrf_token')
        if token_from_form != session.get('csrf_token'):
            return "CSRF token invalid", 400  # Można dodać lepszą obsługę błędów
        
        id_pracownika = int(request.form['id_pracownika'])
        id_produktu = int(request.form['id_produktu'])
        data_sprzedazy = sanitize_input(request.form['data_sprzedazy'])  # Sanitizacja daty sprzedaży
        add_sprzedaz(id_pracownika, id_produktu, data_sprzedazy)
        session.pop('csrf_token', None)
        session['csrf_token'] = generate_csrf_token()

        return redirect(url_for('sprzedaz.sprzedaz', page=page))

    produkty = get_produkty()
    pracownicy = get_sklepowi_pracownicy()

    return render_template(
        'sprzedaz.html',
        sprzedaz=sprzedaz,
        produkty=produkty,
        pracownicy=pracownicy,
        page=page,
        per_page=8,
        start_date=start_date,
        end_date=end_date,
        csrf_token=csrf_token  # Przekazanie tokenu CSRF do szablonu
    )
