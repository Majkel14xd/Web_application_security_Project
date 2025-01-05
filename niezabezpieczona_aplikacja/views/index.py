from flask import Blueprint, render_template,session,redirect,url_for

index_bp = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))  
    return render_template('index.html')
