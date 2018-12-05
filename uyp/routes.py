from flask import render_template, url_for, flash, redirect
from uyp import app, bcrypt, config
from uyp.forms import LoginForm, ApplyForm
from uyp.models import User
from mysql import connector


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.user_id.data, form.category.data, hashed_password)

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

        flash('{0} account created for {1}!'.format(user.category, user.id), 'success')
        return redirect(url_for('home'))
    return render_template('apply.html', title='Apply', form=form)


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
