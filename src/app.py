from flask import Flask
from services.database import init_database
from routes import register_routes


app = Flask(__name__)
init_database(app)
register_routes(app)
