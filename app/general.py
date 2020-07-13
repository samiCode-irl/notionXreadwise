from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('homepage.html')

# To show daily highlights
@app.route('/daily')
def today():
    return render_template('today.html')

# To show all the highlights in the web app database
@app.route('/highlights')
def highlights():
    return render_template('highlights.html')

# To add highlights into the webapp
@app.route('/add')
def add():
    return render_template('add.html')