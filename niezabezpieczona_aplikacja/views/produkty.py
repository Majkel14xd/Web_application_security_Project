from flask import Blueprint, render_template, request, redirect, url_for,session
import sqlite3
import os


produkty_bp = Blueprint('produkty', __name__, template_folder='templates', static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Database'))
db_path = os.path.join(base_dir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(db_path) 
    conn.row_factory = sqlite3.Row
    return conn



# Poprawiona funkcja get_produkty z parametrami
def get_produkty(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM produkty"

    if search_query:
        query += f" WHERE nazwa LIKE '%{search_query}%'"

    query += f" LIMIT {per_page} OFFSET {offset}"

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results



# Poprawiona funkcja add_produkt z parametrami
def add_produkt(nazwa, cena):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"INSERT INTO produkty (nazwa, cena) VALUES ('{nazwa}', {cena})"
    
    cursor.execute(query)
    conn.commit()
    conn.close()


@produkty_bp.route('/produkty', methods=['GET', 'POST'])
def produkty():
    if 'user_id' not in session:
        return redirect(url_for('login.login')) 
    
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    produkty = get_produkty(search_query, per_page=8, page=page)
 
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        cena = float(request.form['cena'])
        add_produkt(nazwa, cena)
        return redirect(url_for('produkty.produkty', page=page, search=search_query))

    return render_template(
        'produkty.html',
        produkty=produkty,
        search_query=search_query,
        page=page,
        per_page=8
    )
