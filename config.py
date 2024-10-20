import os

# Podstawowa konfiguracja (używana przez wszystkie środowiska)
class Config:
    # Sekretne hasło do zabezpieczenia sesji i formularzy
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'

    # Ścieżki do folderów z zasobami
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # MYSQL baza danych
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'jubiler'

    # Konfiguracja sesji (przykład: dłuższa trwałość sesji)
    PERMANENT_SESSION_LIFETIME = 86400  # 24 godziny

    # Inne ustawienia np. email, cache itp.
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

