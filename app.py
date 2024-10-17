from flask import *
import os
from config import *

app = Flask(__name__)

# Wybór konfiguracji na podstawie zmiennej środowiskowej FLASK_ENV
environment = os.getenv('FLASK_ENV', 'development')

if environment == 'development':
    app.config.from_object(DevelopmentConfig)
elif environment == 'production':
    app.config.from_object(ProductionConfig)
elif environment == 'testing':
    app.config.from_object(TestingConfig)

# Przykładowa trasa
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
