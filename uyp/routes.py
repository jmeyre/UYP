from flask import render_template, url_for, flash, redirect, request
from uyp import app, config, bcrypt
from uyp.forms import LoginForm, CreateAccountForm, ProfileForm, AddClassForm, StudentInfo, CreateSessionForm
from uyp.models import User
from mysql import connector
from flask_login import login_user, current_user, logout_user, login_required
import random
from datetime import date
from wtforms.validators import ValidationError


@app.route('/')
@app.route('/home')
@login_required
def home():
    if current_user.category == 'Student':
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM students WHERE students.id = '{0}'".format(current_user.id))

        result = cursor.fetchone()

        if not result:
            return redirect(url_for('student_activate'))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

    return render_template('home.html')


@app.route('/class_search')
@login_required
def class_search():
    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    # For now... (otherwise, make a query that applies filters)
    cursor.execute("SELECT * FROM class")

    classes = cursor.fetchall()

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()
    return render_template('class_search.html', title='Class Search', classes=classes)


@app.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    form = CreateAccountForm()
    if form.validate_on_submit():
        id_chars = "0123456789"
        p_chars = "abcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyz01234567890-_?!#$^"

        id = ''
        for x in range(6):
            id += random.choice(id_chars)

        password = ''
        for x in range(random.randint(8, 12)):
            password += random.choice(p_chars)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id, form.category.data, hashed_password)

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (id, category, pword) VALUES('{0}', '{1}', '{2}')".format(user.id, user.category,
                                                                                         user.pword))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        flash('{0} account created with User ID: {1} and Password: {2}'.format(user.category, user.id, password),
              'success')
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
            "SELECT * FROM users WHERE id = '{0}'".format(form.user_id.data))

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


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    # Prevent students from accessing other students' profiles
    if current_user.category == 'Student' and str(current_user.id) != str(user_id):
        return redirect(url_for('profile', user_id=current_user.id))

    form = ProfileForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET pword = '{0}' WHERE id = '{1}'".format(hashed_password, user_id))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()
    return render_template('profile.html', title='Profile', form=form, user_id=user_id)


@app.route('/student_activate', methods=['GET', 'POST'])
@login_required
def student_activate():
    if current_user.category == 'Student':
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM students WHERE students.id = '{0}'".format(current_user.id))

        result = cursor.fetchone()

        if result:
            return redirect(url_for('home'))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

    form = StudentInfo()

    if form.validate_on_submit():
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (id, fName, mName, lName, suffix, preferred, birthday, gender, race, gradeLevel, expGradYear, street, city, state, zip, email, phone, esl, gt) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}')".format(
                current_user.id, form.fName.data, form.mName.data, form.lName.data, form.suffix.data,
                form.preferred.data, form.bDay.data,
                form.gender.data, form.race.data, form.gradeLevel.data, form.expGradYear.data.year, form.street.data,
                form.city.data, form.state.data,
                form.zip.data, form.email.data, form.phone.data, form.ESL.data, form.GT.data))

        # Sibling query

        # Disability query

        # Health condition query

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        redirect(url_for('home'))

    return render_template('student_activate.html', title='Activate Account', form=form)


@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    conn = connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    resultSessions = cursor.fetchall()
    cursor.execute("SELECT * FROM timeslot")
    resultTimeslots = cursor.fetchall()
    cursor.execute("SELECT * FROM staff")
    resultStaff = cursor.fetchall()
    cursor.close()
    conn.close()

    form = AddClassForm()

    if form.validate_on_submit():
        id_chars = "0123456789"

        id = ''
        for x in range(6):
            id += random.choice(id_chars)

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO class (title, lvl, maxCap, curSize, instructorID, room, timeSlotID, sessionID, classID, price) VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                form.title.data, form.lvl.data, form.maxCap.data, 0, form.instructorID.data, form.room.data,
                form.timeslotID.data, form.sessionID.data, id, form.price.data))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

    return render_template('add_class.html', title='Add Class', form=form, sessions=resultSessions, timeslots=resultTimeslots, staff=resultStaff)


@app.route('/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    form = CreateSessionForm()
    try:
        if form.validate_on_submit() and form.validate_date():
            id_chars = "0123456789"

            id = ''
            for x in range(6):
                id += random.choice(id_chars)

            try:
                # Create the connection to the database
                conn = connector.connect(**config)

                # Create the cursor for the connection
                cursor = conn.cursor()

                cursor.execute("INSERT INTO sessions(id, year, endDate, startDate)"
                               "VALUES ('{0}', '{1}', '{2}', '{3}')".format(id, form.startDate.data.year,
                                                                            form.endDate.data,
                                                                            form.startDate.data))
            except connector.errors.IntegrityError:
                # Session Already Exists
                flash('Session already exists with start/end dates. You might want to edit that session', 'danger')

            # Commit the data to the database
            conn.commit()

            # Close the cursor
            cursor.close()

            # Close the connection to the database
            conn.close()

            flash('Session from {0}/{1}/{2} to {3}/{4}/{5} created!'.format(form.startDate.data.month,
                                                                            form.startDate.data.day,
                                                                            form.startDate.data.year,
                                                                            form.endDate.data.month,
                                                                            form.endDate.data.day,
                                                                            form.endDate.data.year), 'success')
            return redirect(url_for('sessions_search'))

    except ValidationError:
        flash('Start Date cannot be before End Date', 'danger')

    return render_template('create_session.html', title='Create Session', form=form)


@app.route('/sessions_search')
@login_required
def sessions_search():
    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    # For now... (otherwise, make a query that applies filters)
    cursor.execute("SELECT * FROM sessions WHERE endDate > '{0}'".format(date.today()))

    sessions = cursor.fetchall()

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()
    return render_template('sessions_search.html', title='Sessions', sessions=sessions)


@app.route('/edit_session/<session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    # For now... (otherwise, make a query that applies filters)
    cursor.execute("SELECT * FROM sessions WHERE id = '{0}'".format(session_id))

    (id, year, endDate, startDate) = cursor.fetchone()

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()

    form = CreateSessionForm()
    try:
        if form.validate_on_submit() and form.validate_date():
            # Create the connection to the database
            conn = connector.connect(**config)

            # Create the cursor for the connection
            cursor = conn.cursor()

            # For now... (otherwise, make a query that applies filters)
            cursor.execute("UPDATE sessions SET startDate = '{0}', endDate= '{1}' WHERE id = '{2}'".format(
                form.startDate.data, form.endDate.data, session_id))

            # Commit the data to the database
            conn.commit()

            # Close the cursor
            cursor.close()

            # Close the connection to the database
            conn.close()

            flash('Session successfully updated!', 'success')
            return redirect('sessions_search')

    except ValidationError:
        flash('Start Date cannot be before End Date', 'danger')

    return render_template('edit_session.html', title='Edit Session', form=form, session_id=session_id,
                           startDate=startDate, endDate=endDate)


@app.route('/delete_session/<session_id>', methods=['GET', 'POST'])
@login_required
def delete_session(session_id):
    if current_user.category == 'Student':
        #  Don't even indicate to students that this route exists
        #  flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    # For now... (otherwise, make a query that applies filters)
    cursor.execute("DELETE FROM sessions WHERE id = '{0}'".format(session_id))

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()

    flash('Successfully deleted session', 'success')
    return redirect(url_for('sessions_search'))
