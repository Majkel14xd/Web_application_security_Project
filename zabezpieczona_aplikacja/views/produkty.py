from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Blueprint dla produktów
produkty_bp = Blueprint('produkty', __name__, template_folder='templates', static_folder='static')

def get_produkty(search_query=None, per_page=8, page=1):
    offset = (page - 1) * per_page
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()

    query = "SELECT * FROM produkty"
    params = []

    if search_query:
        query += " WHERE nazwa LIKE ?"
        params.append(f"%{search_query}%")

    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results

def add_produkt(nazwa, cena):
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()
    query = "INSERT INTO produkty (nazwa, cena) VALUES (?, ?)"
    cursor.execute(query, (nazwa, cena))
    conn.commit()
    conn.close()

@produkty_bp.route('/produkty', methods=['GET', 'POST'])
def produkty():
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
