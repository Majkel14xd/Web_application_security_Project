from flask import Flask, render_template
from flask_mysqldb import MySQL
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Załaduj konfigurację z klasy Config

mysql = MySQL(app)  # Inicjalizacja MySQL

# Przykładowa trasa
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dane')
def dane():
    # Tworzenie kursora do komunikacji z bazą
    cur = mysql.connection.cursor()  # Użyj instancji mysql

    # Wykonanie zapytania SQL
    cur.execute("SELECT * FROM `tabelatest`")  # Upewnij się, że tabela istnieje
    
    # Pobranie wyników zapytania
    results = cur.fetchall()
    
    # Zwracanie wyników w przeglądarce
    return f"Wyniki zapytania: {results}"

if __name__ == '__main__':
    app.run(debug=True)  # Włączenie trybu debugowania
