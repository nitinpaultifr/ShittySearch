from flask import Flask
from models import db

app = Flask(__name__)

app.secret_key = 'sdfsdid%$^&!@#(fghfrfgeSDFS45$%^)fgh'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:blackwyvern@localhost:3306/search'
db.init_app(app)

from search import routes

