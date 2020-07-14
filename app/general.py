from app import app
from flask import render_template, request, url_for, flash, redirect
from datetime import date
from app.forms import SignUpForm, LoginForm

@app.route('/')
def index():
    return render_template('homepage.html')


# For registeration
@app.route('/SignUp', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

# For Logging into the Account
@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


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

