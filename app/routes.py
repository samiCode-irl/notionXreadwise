from flask import render_template, request, url_for, flash, redirect, abort
from app import app, bcrypt, db
from datetime import date
from app.forms import SignUpForm, LoginForm, HighlightForm
from app.models import User, Highlight
from flask_login import login_user, current_user, logout_user, login_required
from app.notion import get_highlights, get_daily_highlights, compare_highlights, previous_data, get_tags


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('today'))
    return render_template('homepage.html')


# For registeration
@app.route('/SignUp', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    # Dummy token_v2
    dummy_token_v2 = 'a08d5b0a9c758029ce4178b82cb142b0b778f04fb19\
        71c3e8bc8f1b314c1d2b1b3636a874287baccfddd57dbf4912cdb47\
            d62c493bbb067bcbdb0e72a3fd890a4469752808122bc650c6033ab563'

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        if form.token_v2.data != '':
            user.token_v2 = form.token_v2.data
        else:
            user.token_v2 = dummy_token_v2
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully. You can log in now.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


# For Logging into the Account
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


# To show daily highlights
@app.route('/daily')
@login_required
def today():
    today = date.today()
    highlights = get_daily_highlights(5)
    highlights = compare_highlights(highlights, today)

    return render_template('today.html', highlights=highlights, today=today.strftime("%b %d, %Y"))


# To show all the highlights in the web app database
@app.route('/highlights')
@login_required
def highlights():
    page = request.args.get('page', 1, type=int)
    highlights = Highlight.query.filter(
        Highlight.user_id == current_user.id).order_by(Highlight.id.desc()).paginate(page=page, per_page=5)
    return render_template('highlights.html', highlights=highlights)


# Highlights Individually
@app.route("/highlight/<int:highlight_id>")
@login_required
def highlight(highlight_id):
    highlight = Highlight.query.get_or_404(highlight_id)
    if highlight.user_id != current_user.id:
        abort(403)
    return render_template('highlight.html', highlight=highlight)


# To create new highlight
@app.route("/highlight/new", methods=['GET', 'POST'])
@login_required
def new_highlight():
    form = HighlightForm()
    if form.validate_on_submit():
        highlight = Highlight(title=form.title.data, author=form.author.data, highlight=form.highlight.data,
                              tags=form.tags.data, user_id=current_user.id)
        db.session.add(highlight)
        db.session.commit()
        flash('Your highlight has been created!', 'success')
        return redirect(url_for('highlights'))
    return render_template('create_highlight.html', title='New', form=form, legend="Create New")


# To update Highlight
@app.route('/highlight/<int:highlight_id>/update', methods=['GET', 'POST'])
@login_required
def update_highlight(highlight_id):
    highlight = Highlight.query.get_or_404(highlight_id)
    if highlight.user_id != current_user.id:
        abort(403)

    form = HighlightForm()
    if form.validate_on_submit():
        highlight.title = form.title.data
        highlight.author = form.author.data
        highlight.highlight = form.highlight.data
        highlight.tags = form.tags.data
        db.session.commit()
        flash('Your Highlight has been updated!', 'success')
        return redirect(url_for('highlight', highlight_id=highlight.id))

    elif request.method == 'GET':
        form.title.data = highlight.title
        form.author.data = highlight.author
        form.highlight.data = highlight.highlight
        form.tags.data = highlight.tags

    return render_template('create_highlight.html', title='Update', form=form, legend='Update Highlight')


# To delete highlight
@app.route('/highlight/<int:highlight_id>/delete', methods=['POST'])
@login_required
def delete_highlight(highlight_id):
    highlight = Highlight.query.get_or_404(highlight_id)
    if highlight.curator != current_user:
        abort(403)

    db.session.delete(highlight)
    db.session.commit()
    flash('Your highlight is deleted!', 'success')
    return redirect(url_for('highlights'))


# To add highlights into the webapp
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        get_highlights(request.form.get('link'))
        flash('Highlights added successfully.', 'success')

    return redirect(url_for('add'))


# for logging out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# For tag variables
@app.route('/tag/<string:tag>')
@login_required
def tags(tag):

    page = request.args.get('page', 1, type=int)
    current_tag = get_tags()

    if tag.lower() not in current_tag:
        abort(404)
    elif tag.lower() in current_tag:
        current_tag = tag.lower()

    highlights = Highlight.query.filter(Highlight.user_id == current_user.id)\
        .order_by(Highlight.id.desc()).all()
    return render_template('tag_highlights.html', highlights=highlights, tag=current_tag)


# Error Handlers
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
