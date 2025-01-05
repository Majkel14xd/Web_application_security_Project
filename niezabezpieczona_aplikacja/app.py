from flask import Flask
from views.index import index_bp
from views.login import login_bp
from views.logout import logout_bp
from views.dashboard import dashboard_bp
from views.pracownicy import pracownicy_bp
from views.sprzedaz import sprzedaz_bp
from views.produkty import produkty_bp
app = Flask(__name__)
def create_app():
    app.secret_key = 'MLRK'
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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)