from flask import render_template, url_for, flash, redirect, request
from uyp import app, config, bcrypt
from uyp.forms import LoginForm, CreateAccountForm, AccountForm
from uyp.models import User
from mysql import connector
from flask_login import login_user, current_user, logout_user, login_required
import random


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    print("it got here")
    if form.validate_on_submit():
        id_chars = "0123456789"
        p_chars = "abcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyz01234567890-_?!#$^"

        id = ''
        for x in range(7):
            id += random.choice(id_chars)

        password = ''
        for x in range(random.randint(8,12)):
            password += random.choice(p_chars)

        print('{0} {1}'.format(id, password))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id, form.category.data, hashed_password)

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (ID, category, pword) VALUES({0}, '{1}', '{2}')".format(user.id, user.category, user.pword))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        flash('{0} account created with User ID: {1} and Password: {2}'.format(user.category, user.id, password), 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html', title='Create Account', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE ID = {0}".format(form.user_id.data))

        result = cursor.fetchone()

        if result:
            user = User(result[0], result[1], result[2])

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        if result and user and bcrypt.check_password_hash(user.pword, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in, {0}!'.format(user.id), 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Incorrect user id or password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET pword = '{0}'".format(hashed_password))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()
    return render_template('account.html', title='Account', form=form)
