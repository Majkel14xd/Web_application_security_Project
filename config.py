import os

# Podstawowa konfiguracja (używana przez wszystkie środowiska)
class Config:
    # Sekretne hasło do zabezpieczenia sesji i formularzy
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'

    # Ścieżki do folderów z zasobami
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Baza danych SQLite (do developmentu lub prostych aplikacji)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Wyłączenie śledzenia modyfikacji

    # Konfiguracja sesji (przykład: dłuższa trwałość sesji)
    PERMANENT_SESSION_LIFETIME = 86400  # 24 godziny

    # Inne ustawienia np. email, cache itp.
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Konfiguracja do developmentu (większe możliwości debugowania, baza SQLite)
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    ENV = 'development'

# Konfiguracja do produkcji (mniej szczegółowe błędy, baza danych produkcyjna)
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///prod.db'
    ENV = 'production'

# Konfiguracja do testów (baza testowa, minimalizacja logów)
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False  # Wyłączenie CSRF podczas testów
    ENV = 'testing'
