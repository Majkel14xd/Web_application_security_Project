from flask import Flask, request, abort
from views.index import index_bp
from views.login import login_bp
from views.logout import logout_bp
from views.dashboard import dashboard_bp
from views.pracownicy import pracownicy_bp
from views.sprzedaz import sprzedaz_bp
from views.produkty import produkty_bp
from views.fake_produkty import fake_produkty_bp

import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization
import os
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)

# Pobierz wartość zmiennej EXPECTED_CERT_HASH
EXPECTED_CERT_HASH = os.getenv("EXPECTED_CERT_HASH")

def create_app():
    app.secret_key= os.urandom(24)
    app.jinja_env.autoescape = False
    # Rejestracja Blueprinta dla strony głównej
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp) 
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pracownicy_bp ,url_prefix="/dashboard")
    app.register_blueprint(sprzedaz_bp ,url_prefix="/dashboard")
    app.register_blueprint(produkty_bp ,url_prefix="/dashboard")
    app.register_blueprint(fake_produkty_bp ,url_prefix="/dashboard")
    return app


app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=True,
)

def get_cert_hash(cert_pem):
    """Funkcja do obliczania hasza certyfikatu"""
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'))
    cert_der = cert.public_bytes(serialization.Encoding.DER)
    cert_hash = hashlib.sha256(cert_der).hexdigest().upper()
    return cert_hash

def load_cert_from_file(file_path):
    """Załaduj certyfikat z pliku"""
    with open(file_path, 'r') as cert_file:
        cert_pem = cert_file.read()
    return cert_pem

@app.before_request
def check_cert():
    """Sprawdzanie certyfikatu przy każdym połączeniu"""
    if request.url.startswith('https://'):
        # Załaduj certyfikat z pliku cert.pem
        cert_pem = load_cert_from_file('Certs/server.crt')  # Ścieżka do pliku certyfikatu

        if cert_pem:
            # Obliczanie hasza certyfikatu
            cert_hash = get_cert_hash(cert_pem)  # Obliczanie hasza certyfikatu
            if cert_hash != EXPECTED_CERT_HASH:
                abort(403, description="Certificate does not match the expected pin.")
        else:
            abort(403, description="No certificate provided.")

@app.after_request
def after_request_func(response):
    response.headers['Public-Key-Pins'] = 'pin-sha256="base64-encoded-key"; max-age=5184000; includeSubDomains'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"

    return response


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, ssl_context=('Certs/server.crt', 'Certs/server.key',), host='0.0.0.0', port=5000)
