from flask import render_template, url_for, flash, redirect, request
from uyp import app, config, bcrypt
from uyp.forms import LoginForm, CreateAccountForm, ProfileForm, AddClassForm, StudentInfo, CreateSessionForm
from uyp.models import User, Student, Class
from mysql import connector
from flask_login import login_user, current_user, logout_user, login_required
import random
from datetime import date
from wtforms.validators import ValidationError


@app.route('/')
@app.route('/home')
@login_required
def home():
    user = None
    classes = None
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(current_user.id))

        user = cursor.fetchone()

        if not user:
            return redirect(url_for('student_activate'))

        cursor.execute("SELECT c.*, i.fName, i.lName "
                       "FROM takes t, class c, staff i "
                       "WHERE t.studentID = '{0}' "
                       "AND c.instructorID = i.id "
                       "AND t.classID = c.classID".format(current_user.id))

        classes = cursor.fetchall()

        # Commit the data to the database
        conn.commit()
        cursor.close()
        conn.close()

    elif current_user.category == 'Staff':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM staff WHERE id = '{0}'".format(current_user.id))

        user = cursor.fetchone()

        cursor.execute("SELECT c.*, i.fName, i.lName "
                       "FROM  class c, staff i "
                       "WHERE c.instructorID = '{0}'".format(current_user.id))

        classes = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

    return render_template('home.html', user=user, classes=classes)


@app.route('/class_search')
@login_required
def class_search():
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(current_user.id))
        result = cursor.fetchone()

        if not result:
            flash('You need to activate your account first!', 'danger')
            return redirect(url_for('student_activate'))

        conn.commit()
        cursor.close()
        conn.close()

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT c1.*, i.fName , i.lName "
                       "FROM class c1, sessions s1, staff i "
                       "WHERE c1.sessionID = s1.id "
                       "AND c1.instructorID = i.id "
                       "AND s1.startDate  > '{0}' "
                       "AND c1.curSize < c1.maxCap "
                       "AND c1.classID NOT IN "
                       "(SELECT c.classID FROM class c, takes t, sessions s WHERE t.classID = c.classID "
                       "AND c.sessionID = s.id "
                       "AND s.startDate > '{0}' AND c.curSize < c.maxCap)".format(date.today()))
        classes = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

    else:

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT c.*, i.fName, i.lName FROM class c, staff i WHERE c.instructorID = i.id")

        classes = cursor.fetchall()

        conn.commit()
        cursor.close()
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

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (id, category, pword) VALUES('{0}', '{1}', '{2}')".format(user.id, user.category,
                                                                                         user.pword))

        conn.commit()
        cursor.close()
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

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = '{0}'".format(form.user_id.data))
        result = cursor.fetchone()

        if result:
            user = User(result[0], result[1], result[2])

        conn.commit()
        cursor.close()
        conn.close()

        if result and user and bcrypt.check_password_hash(user.pword, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
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

    if current_user.category == 'Student':
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(current_user.id))

        result = cursor.fetchone()

        if not result:
            return redirect(url_for('student_activate'))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

    # only executes if student activation form has been filled out

    # get the category of the profile we're viewing
    conn = connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM users WHERE id = '{0}'".format(user_id))
    category = cursor.fetchone()
    category = category[0]

    # Create student object
    if category == 'Student':
        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(user_id))
        result = Student(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                         result[8], result[9], result[10], result[11], result[12], result[13], result[14],
                         result[15], result[16], result[17], result[18])

    elif category == 'Staff':
        cursor.execute("SELECT * FROM staff WHERE id = '{0}'".format(user_id))
        # Create Staff Object

    form = ProfileForm()
    sform = StudentInfo()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET pword = '{0}' WHERE id = '{1}'".format(hashed_password, user_id))

        conn.commit()
        cursor.close()
        conn.close()

    if sform.validate_on_submit():

        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        # if a student entered info
        if category == 'Student':
            # needs to be update query
            cursor.execute("UPDATE students SET fName = '{1}', mName = '{2}', lName = '{3}', suffix = '{4}', "
                           "preferred = '{5}', birthday = '{6}', gender = '{7}', race = '{8}', gradeLevel = '{9}', "
                           "expGradYear = '{10}', street = '{11}', city = '{12}', state='{13}', zip='{14}', email = '{15}',"
                           " phone = '{16}', esl='{17}', gt = '{18}' WHERE id = '{0}'".format(user_id, form.fName.data,
                                                                                              form.mName.data,
                                                                                              form.lName.data,
                                                                                              form.suffix.data,
                                                                                              form.preferred.data,
                                                                                              form.bDay.data,
                                                                                              form.gender.data,
                                                                                              form.race.data,
                                                                                              form.gradeLevel.data,
                                                                                              form.expGradYear.data.year,
                                                                                              form.street.data,
                                                                                              form.city.data,
                                                                                              form.state.data,
                                                                                              form.zip.data,
                                                                                              form.email.data,
                                                                                              form.phone.data,
                                                                                              form.ESL.data,
                                                                                              form.GT.data))

        # if staff info is entered
        elif category == 'Staff':
            # needs to  be update query
            cursor.execute("UPDATE staff SET WHERE id = '{0}'".format(user_id))
            result = cursor.fetchone()

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

    return render_template('profile.html', title='Profile', form=form, sform=sform, user_id=user_id, result=result,
                           category=category)


@app.route('/student_activate', methods=['GET', 'POST'])
@login_required
def student_activate():
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM students WHERE students.id = '{0}'".format(current_user.id))
        result = cursor.fetchone()

        if result:
            return redirect(url_for('home'))

        conn.commit()
        cursor.close()
        conn.close()

    form = StudentInfo()

    if form.validate_on_submit():

        conn = connector.connect(**config)
        cursor = conn.cursor()

        year = 0
        if form.expGradYear.data:
            year = form.expGradYear.data.year

        cursor.execute(
            "INSERT INTO students (id, fName, mName, lName, suffix, preferred, birthday, gender, race, gradeLevel, expGradYear, street, city, state, zip, email, phone, esl, gt) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', {10}, '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}')".format(
                current_user.id, form.fName.data, form.mName.data, form.lName.data, form.suffix.data,
                form.preferred.data, form.bDay.data,
                form.gender.data, form.race.data, form.gradeLevel.data, year, form.street.data,
                form.city.data, form.state.data,
                form.zip.data, form.email.data, form.phone.data, form.ESL.data if form.ESL.data is None else 0,
                form.GT.data if form.GT.data is None else 0))

        # Disability query
        if form.disability.data == 'on':
            cursor.execute(
                "INSERT INTO disability (studentID, disability) VALUES ('{0}', '{1}')".format(current_user.id,
                                                                                              form.disabilityDesc.data))

        # Health condition query
        if form.healthConds.data == 'on':
            cursor.execute(
                "INSERT INTO healthcondition (studentID, cond, descript) VALUES ('{0}', '{1}', '{2}')".format(
                    current_user.id, form.healthCondsCond.data, form.healthCondsDesc.data))

        # Guardian1 query
        cursor.execute(
            "INSERT INTO guardian (studentID, fName, mName, lName, phone, email, street, city, state, zip) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                current_user.id, form.guardian1_fName.data, form.guardian1_mName.data, form.guardian1_lName.data,
                form.guardian1_phone.data, form.guardian1_email.data, form.guardian1_street.data,
                form.guardian1_city.data, form.guardian1_state.data, form.guardian1_zip.data))

        # Guardian2 query
        if form.guardian2_prompt.data == 'on':
            cursor.execute(
                "INSERT INTO guardian (studentID, fName, mName, lName, phone, email, street, city, state, zip) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                    current_user.id, form.guardian2_fName.data, form.guardian2_mName.data, form.guardian2_lName.data,
                    form.guardian2_phone.data, form.guardian2_email.data, form.guardian2_street.data,
                    form.guardian2_city.data, form.guardian2_state.data, form.guardian2_zip.data))

        # Sibling query

        conn.commit()
        cursor.close()
        conn.close()

        flash('Successfully activated your account!', 'success')
        return redirect(url_for('home'))

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

    conn.commit()
    cursor.close()
    conn.close()

    form = AddClassForm()

    if form.validate_on_submit():
        id_chars = "0123456789"

        id = ''
        for x in range(6):
            id += random.choice(id_chars)

        conn = connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO class (title, lvl, maxCap, curSize, instructorID, room, timeSlotID, sessionID, classID, price) VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                form.title.data, form.lvl.data, form.maxCap.data, 0, form.instructorID.data, form.room.data,
                form.timeslotID.data, form.sessionID.data, id, form.price.data))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Class Added!', 'success')
        return redirect(url_for('class_search'))

    return render_template('add_class.html', title='Add Class', form=form, sessions=resultSessions,
                           timeslots=resultTimeslots, staff=resultStaff)


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
                conn = connector.connect(**config)
                cursor = conn.cursor()

                cursor.execute("INSERT INTO sessions(id, year, endDate, startDate)"
                               "VALUES ('{0}', '{1}', '{2}', '{3}')".format(id, form.startDate.data.year,
                                                                            form.endDate.data,
                                                                            form.startDate.data))
            except connector.errors.IntegrityError:
                # Session Already Exists
                flash('Session already exists with start/end dates. You might want to edit that session', 'danger')

            conn.commit()
            cursor.close()
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
    conn = connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions WHERE endDate > '{0}'".format(date.today()))
    sessions = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('sessions_search.html', title='Sessions', sessions=sessions)


@app.route('/edit_session/<session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    conn = connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions WHERE id = '{0}'".format(session_id))
    (id, year, endDate, startDate) = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    form = CreateSessionForm()
    try:
        if form.validate_on_submit() and form.validate_date():
            conn = connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("UPDATE sessions SET startDate = '{0}', endDate= '{1}' WHERE id = '{2}'".format(
                form.startDate.data, form.endDate.data, session_id))

            conn.commit()
            cursor.close()
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

    conn = connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sessions WHERE id = '{0}'".format(session_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Successfully deleted session', 'success')

    return redirect(url_for('sessions_search'))


@app.route('/delete_class/<class_id>', methods=['GET', 'POST'])
@login_required
def delete_class(class_id):
    if current_user.category == 'Student':
        #  Don't even indicate to students that this route exists
        #  flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    conn = connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM class WHERE classID = '{0}'".format(class_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Successfully deleted class!', 'success')

    return redirect(url_for('class_search'))


@app.route('/register_class/<class_id>')
@login_required
def register_class(class_id):
    if current_user.category == 'Student':
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("INSERT INTO takes(studentID, classID) VALUES ('{0}', '{1}')".format(current_user.id, class_id))
        cursor.execute("SELECT curSize FROM class WHERE classID = '{0}'".format(class_id))

        class_size = cursor.fetchone()

        # Increment the class' curSize
        cursor.execute("UPDATE class SET curSize = {0} WHERE classID = '{1}'".format(class_size[0] + 1, class_id))

        cursor.execute("SELECT title FROM class WHERE classID = '{0}'".format(class_id))
        title = cursor.fetchone()

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        flash('Successfully registered for {0}!'.format(title[0]), 'success')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('class_search'))


@app.route('/edit_class/<class_id>', methods=['GET', 'POST'])
@login_required
def edit_class(class_id):
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
    cursor.execute("SELECT * FROM class WHERE classID = '{0}'".format(class_id))
    resultClass = cursor.fetchone()
    resultClass = Class(resultClass[0], resultClass[1], resultClass[2], resultClass[3], resultClass[4], resultClass[5],
                        resultClass[6], resultClass[7], resultClass[8], resultClass[9])

    cursor.close()
    conn.close()

    form = AddClassForm()

    # after submitting
    if form.validate_on_submit():
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE class SET title='{0}', lvl='{1}', maxCap='{2}', instructorID='{3}', room='{4}', "
            "timeSlotID='{5}', sessionID='{6}', price='{7}'".format(
                form.title.data, form.lvl.data, form.maxCap.data, form.instructorID.data, form.room.data,
                form.timeslotID.data, form.sessionID.data, form.price.data))

        # Commit the data to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Close the connection to the database
        conn.close()

        flash('Class Edited!', 'success')
        return redirect(url_for('class_search'))

    return render_template('edit_class.html', title='Edit Class', form=form, sessions=resultSessions,
                           timeslots=resultTimeslots, staff=resultStaff, resultClass=resultClass)
