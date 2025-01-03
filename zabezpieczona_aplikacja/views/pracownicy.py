from flask import Blueprint, Flask, render_template, request, redirect, url_for
import sqlite3

pracownicy_bp = Blueprint('pracownicy', __name__, template_folder='templates', static_folder='static')

# Funkcja do pobierania pracowników z bazy danych
def get_pracownicy(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()

    query = "SELECT * FROM pracownicy"
    params = []

    if search_query:
        query += " WHERE imie LIKE ? OR nazwisko LIKE ?"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results

# Funkcja do dodawania pracowników do bazy danych
def add_pracownik(imie, nazwisko, stanowisko):
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()
    query = "INSERT INTO pracownicy (imie, nazwisko, stanowisko) VALUES (?, ?, ?)"
    cursor.execute(query, (imie, nazwisko, stanowisko))
    conn.commit()
    conn.close()

# Widok dla strony pracowników
@pracownicy_bp.route('/pracownicy', methods=['GET', 'POST'])
def pracownicy():
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
