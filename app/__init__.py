from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Super Secret Key'

from app import general
from app import forms
