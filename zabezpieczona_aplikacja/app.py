from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zmienna sekretna do sesji

# Funkcja do połączenia z bazą danych
def get_db_connection():
    conn = sqlite3.connect('Database/database.db')  # Ścieżka do bazy danych SQLite
    conn.row_factory = sqlite3.Row
    return conn

# Strona logowania
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        haslo = request.form['haslo']
        
        # Szyfrowanie hasła przed porównaniem
        hashed_password = hashlib.sha256(haslo.encode()).hexdigest()

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM konto WHERE login = ? AND haslo = ?', (login, hashed_password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))  # Przekierowanie po zalogowaniu
        else:
            flash('Błędny login lub hasło', 'error')

    return render_template('index.html')

# Strona główna po zalogowaniu
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Przekierowanie do logowania jeśli użytkownik nie jest zalogowany
    
    return 'Witaj na panelu administracyjnym!'

# Strona wylogowania
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
