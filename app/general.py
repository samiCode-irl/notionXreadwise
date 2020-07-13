from app import app
from flask import render_template, request
from datetime import date

@app.route('/')
def index():
    return render_template('homepage.html')

# To show daily highlights
@app.route('/daily')
def today():
    today = date.today()
    return render_template('today.html', today=today.strftime("%b %d, %Y"))

# To show all the highlights in the web app database
@app.route('/highlights')
def highlights():
    return render_template('highlights.html')

# To add highlights into the webapp
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')

    return render_template('add.html')

