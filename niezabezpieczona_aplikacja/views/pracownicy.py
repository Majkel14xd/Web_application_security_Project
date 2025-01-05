from flask import Blueprint, Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

pracownicy_bp = Blueprint('pracownicy', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(db_path) 
    conn.row_factory = sqlite3.Row
    return conn

# Funkcja do pobierania pracowników z bazy danych
def get_pracownicy(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM pracownicy"
    
    if search_query:
        query += f" WHERE imie LIKE '%{search_query}%' OR nazwisko LIKE '%{search_query}%'"

    query += f" LIMIT {per_page} OFFSET {offset}"

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

# Funkcja do dodawania pracowników do bazy danych
def add_pracownik(imie, nazwisko, stanowisko):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO pracownicy (imie, nazwisko, stanowisko) VALUES ('{imie}', '{nazwisko}', '{stanowisko}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

# Widok dla strony pracowników
@pracownicy_bp.route('/pracownicy', methods=['GET', 'POST'])
def pracownicy():
    if 'user_id' not in session:
        return redirect(url_for('login.login')) 

    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    pracownicy = get_pracownicy(search_query, per_page=8, page=page)

    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        stanowisko = request.form['stanowisko']
        add_pracownik(imie, nazwisko, stanowisko)
        return redirect(url_for('pracownicy.pracownicy', page=page, search=search_query)) 
    
    return render_template(
        'pracownicy.html',
        pracownicy=pracownicy,
        search_query=search_query,
        page=page,
        per_page=8
    )
