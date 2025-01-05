from flask import Blueprint, render_template

# Tworzymy Blueprint do fake attack
fake_produkty_bp = Blueprint('fake_produkty', __name__, template_folder='templates', static_folder='static')

@fake_produkty_bp.route('/fake_produkty')
def fake_produkty():
    # Renderujemy plik HTML z folderu templates
    return render_template('fake_produkty.html')
