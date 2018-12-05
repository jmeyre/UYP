from flask import render_template, url_for, flash, redirect
from uyp import app
from uyp.forms import LoginForm
# from uyp.models import user,etc.

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


""" (No need to apply online)
@uyp.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        flash('Account created for {0}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('apply.html', title='Apply', form=form)
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'username' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Incorrect username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)
