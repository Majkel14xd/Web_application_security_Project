from flask import Flask, request, abort
from views.index import index_bp
from views.login import login_bp
from views.logout import logout_bp
from views.dashboard import dashboard_bp
from views.pracownicy import pracownicy_bp
from views.sprzedaz import sprzedaz_bp
from views.produkty import produkty_bp
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

def create_app():
    app.secret_key="MLRK"
    app.jinja_env.autoescape = False
    # Rejestracja Blueprinta dla strony głównej
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp) 
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pracownicy_bp ,url_prefix="/dashboard")
    app.register_blueprint(sprzedaz_bp ,url_prefix="/dashboard")
    app.register_blueprint(produkty_bp ,url_prefix="/dashboard")
    return app


EXPECTED_CERT_HASH = "11C0A2146058C6DF3C10656234B80AF46CE5AD6FE9702FF96A15CD9CCF4EF9F2"

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
        cert_pem = load_cert_from_file('Cert/server.crt')  # Ścieżka do pliku certyfikatu

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
    app.run(debug=True, ssl_context=('Cert/server.crt', 'Cert/server.key'), host='0.0.0.0', port=5000)
