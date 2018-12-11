from flask import render_template, url_for, flash, redirect, request
from uyp import app, config, bcrypt
from uyp.forms import LoginForm, CreateAccountForm, ProfileForm, AddClassForm, StudentInfo, CreateSessionForm, \
    StaffForm, SiblingForm
from uyp.models import User, Student, Class, Staff, Disability, HealthCondition, Guardian, School
from mysql import connector
from flask_login import login_user, current_user, logout_user, login_required
import random
from datetime import date
from wtforms.validators import ValidationError


@app.route('/')
@app.route('/home')
@login_required
def home():
    student = None
    staff = None
    classes = None
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(current_user.id))

        stu = cursor.fetchone()

        if not stu[1]:
            return redirect(url_for('student_activate'))

        student = Student(stu[0], stu[1], stu[2], stu[3], stu[4], stu[5], stu[6], stu[7], stu[8], stu[9], stu[10],
                          stu[11], stu[12], stu[13], stu[14], stu[15], stu[16], stu[17], stu[18], stu[19], stu[20],
                          stu[21], stu[22], stu[23], stu[24], stu[25], stu[26])

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

        sta = cursor.fetchone()

        if not sta:
            return redirect(url_for('staff_activate'))

        staff = Staff(sta[0], sta[1], sta[2], sta[3], sta[4], sta[5], sta[6], sta[7], sta[8], sta[9], sta[10])

        cursor.execute("SELECT c.*, i.fName, i.lName "
                       "FROM  class c, staff i "
                       "WHERE c.instructorID = i.id AND c.instructorID = '{0}'".format(current_user.id))

        classes = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

    return render_template('home.html', student=student, staff=staff, classes=classes)


@app.route('/class_search')
@login_required
def class_search():
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT fName FROM students WHERE id = '{0}'".format(current_user.id))

        result = cursor.fetchone()

        if not result[0]:
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
                       "AND s.startDate > '{0}' AND c.curSize < c.maxCap AND t.studentID = '{1}')".format(date.today(), current_user.id))
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

        if user.category == 'Student':
            currentDate = date.today()

            cursor.execute(
                "INSERT INTO students (id, acceptedYear, acceptedBy, bill) VALUES('{0}', '{1}', '{2}', '{3}')".format(
                    user.id, currentDate.year, current_user.id, 0))

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
    student = None
    disability = None
    healthCondition = None
    guardian1 = None
    guardian2 = None
    staff = None
    school = None
    # Prevent students from accessing other students' profiles
    if current_user.category == 'Student' and str(current_user.id) != str(user_id):
        return redirect(url_for('profile', user_id=current_user.id))

    if current_user.category == 'Student':
        # Create the connection to the database
        conn = connector.connect(**config)

        # Create the cursor for the connection
        cursor = conn.cursor()

        cursor.execute("SELECT fName FROM students WHERE id = '{0}'".format(current_user.id))

        result = cursor.fetchone()

        if not result[0]:
            flash('You need to activate your account first!', 'danger')
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
    cat = cursor.fetchone()
    category = cat[0]

    # Create student object
    if category == 'Student':
        cursor.execute("SELECT * FROM students WHERE id = '{0}'".format(user_id))
        stu = cursor.fetchone()

        if stu:
            student = Student(stu[0], stu[1], stu[2], stu[3], stu[4], stu[5], stu[6], stu[7], stu[8], stu[9], stu[10],
                              stu[11], stu[12], stu[13], stu[14], stu[15], stu[16], stu[17], stu[18], stu[19], stu[20],
                              stu[21], stu[22], stu[23], stu[24], stu[25], stu[26])

        cursor.execute("SELECT * FROM disability WHERE studentID = '{0}'".format(user_id))
        # Only one disability for now...
        dis = cursor.fetchone()

        if dis:
            disability = Disability(dis[0], dis[1])

        cursor.execute("SELECT * FROM healthcondition WHERE studentID = '{0}'".format(user_id))
        # Only one disability for now...
        hea = cursor.fetchone()

        if hea:
            healthCondition = HealthCondition(hea[0], hea[1], hea[2])

        cursor.execute("SELECT * FROM guardian WHERE studentID = '{0}'".format(user_id))
        # Only one disability for now...
        guardians = cursor.fetchall()

        if guardians:
            if guardians[0]:
                guardian1 = Guardian(guardians[0][0], guardians[0][1], guardians[0][2], guardians[0][3], guardians[0][4],
                                     guardians[0][5], guardians[0][6], guardians[0][7], guardians[0][8], guardians[0][9])

            if len(guardians) > 1:
                guardian2 = Guardian(guardians[1][0], guardians[1][1], guardians[1][2], guardians[1][3], guardians[1][4],
                                     guardians[1][5], guardians[1][6], guardians[1][7], guardians[1][8], guardians[1][9])

        cursor.execute("SELECT * FROM school WHERE studentID = '{0}'".format(user_id))
        sch = cursor.fetchone()

        if sch:
            school = School(sch[0], sch[1], sch[2], sch[3], sch[4])

    elif category == 'Staff':
        cursor.execute("SELECT * FROM staff WHERE id = '{0}'".format(user_id))
        sta = cursor.fetchone()

        if sta:
            staff = Staff(sta[0], sta[1], sta[2], sta[3], sta[4], sta[5], sta[6], sta[7], sta[8], sta[9], sta[10])

    form = ProfileForm()
    sform = StudentInfo()
    staffForm = StaffForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if not form.new_password.data == '':
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

                conn = connector.connect(**config)
                cursor = conn.cursor()

                cursor.execute("UPDATE users SET pword = '{0}' WHERE id = '{1}'".format(hashed_password, user_id))

                conn.commit()
                cursor.close()
                conn.close()

                flash('Password changed successfully!', 'success')

        if sform.validate_on_submit():

            # Create the connection to the database
            conn = connector.connect(**config)

            # Create the cursor for the connection
            cursor = conn.cursor()

            esl_data = sform.ESL.data
            if esl_data == 'on':
                esl_data = 1
            else:
                esl_data = 0

            gt_data = sform.GT.data
            if gt_data == 'on':
                gt_data = 1
            else:
                gt_data = 0

            # needs to be update query
            cursor.execute("UPDATE students SET fName = '{1}', mName = '{2}', lName = '{3}', suffix = '{4}', "
                           "preferred = '{5}', birthday = '{6}', gender = '{7}', race = '{8}', gradeLevel = '{9}', "
                           "expGradDate = '{10}', street = '{11}', city = '{12}', state='{13}', zip='{14}', "
                           "email = '{15}', phone = '{16}', esl='{17}', gt = '{18}', otherInfo = '{19}', "
                           "expSchool = '{20}' WHERE id = '{0}'".format(user_id, sform.fName.data, sform.mName.data,
                                                                        sform.lName.data, sform.suffix.data,
                                                                        sform.preferred.data, sform.bDay.data,
                                                                        sform.gender.data, sform.race.data,
                                                                        sform.gradeLevel.data, sform.expGradDate.data,
                                                                        sform.street.data, sform.city.data,
                                                                        sform.state.data, sform.zip.data,
                                                                        sform.email.data, sform.phone.data, esl_data,
                                                                        gt_data, sform.otherInfo.data,
                                                                        sform.expSchool.data))

            # disability
            cursor.execute("SELECT * FROM disability WHERE studentID = '{0}'".format(user_id))

            stuDis = cursor.fetchone()

            if stuDis:
                if stuDis[1] == '':
                    cursor.execute("DELETE FROM disability WHERE studentID = '{0}'".format(user_id))
                else:
                    cursor.execute("UPDATE disability SET disability = '{1}' WHERE studentID = '{0}'".format(user_id,
                                                                                                             sform.disabilityDesc.data))
            else:
                cursor.execute("INSERT INTO disability (studentID, disability) VALUES('{0}', '{1}')".format(user_id,
                                                                                                            sform.disabilityDesc.data))

            # health condition
            cursor.execute("SELECT * FROM healthcondition WHERE studentID = '{0}'".format(user_id))

            stuHea = cursor.fetchone()

            if stuHea:
                if stuHea[1] == '' and stuHea[2] == '':
                    cursor.execute("DELETE FROM healthcondition WHERE studentID = '{0}'".format(user_id))
                else:
                    cursor.execute("UPDATE healthcondition "
                                   "SET cond = '{1}', descript = '{2}' WHERE studentID = '{0}'".format(user_id,
                                                                                                       sform.healthCondsCond.data,
                                                                                                       sform.healthCondsDesc.data))
            else:
                cursor.execute(
                    "INSERT INTO healthcondition (studentID, cond, descript) VALUES('{0}', '{1}', '{2}')".format(
                        user_id, sform.healthCondsCond.data, sform.healthCondsDesc.data))

            # school
            cursor.execute(
                "UPDATE school SET name = '{1}', type = '{2}', district = '{3}' WHERE studentID = '{0}'".format(
                    user_id, sform.expSchool.data, sform.expSchoolType.data, sform.expSchoolDistrict.data))
            cursor.execute(
                "UPDATE students SET expSchool = '{1}' WHERE id = '{0}'".format(user_id, sform.expSchool.data))

            # gt

            # Commit the data to the database
            conn.commit()

            # Close the cursor
            cursor.close()

            # Close the connection to the database
            conn.close()
            flash('Info updated successfully!', 'success')

        elif staffForm.validate_on_submit():
            # Create the connection to the database
            conn = connector.connect(**config)

            # Create the cursor for the connection
            cursor = conn.cursor()

            # needs to  be update query
            cursor.execute("UPDATE staff SET fName='{1}', mName='{2}', lName='{3}', suffix='{4}', street='{5}', "
                           "city='{6}', state='{7}', zip='{8}', email='{9}', phone='{10}' WHERE id='{0}'".format(
                user_id, staffForm.fName.data, staffForm.mName.data, staffForm.lName.data, staffForm.suffix.data,
                staffForm.street.data, staffForm.city.data, staffForm.state.data, staffForm.zip.data,
                staffForm.email.data, staffForm.phone.data))

            # Commit the data to the database
            conn.commit()

            # Close the cursor
            cursor.close()

            # Close the connection to the database
            conn.close()
            flash('Info updated successfully!', 'success')
        return redirect(url_for('profile', user_id=user_id))

    return render_template('profile.html', title='Profile', form=form, sform=sform, staffForm=staffForm,
                           user_id=user_id, category=category, student=student, disability=disability,
                           healthCondition=healthCondition, guardian1=guardian1, guardian2=guardian2, staff=staff,
                           school=school)


@app.route('/student_activate', methods=['GET', 'POST'])
@login_required
def student_activate():
    if current_user.category == 'Student':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT fName FROM students WHERE students.id = '{0}'".format(current_user.id))
        result = cursor.fetchone()

        if result[0]:
            return redirect(url_for('home'))

        conn.commit()
        cursor.close()
        conn.close()

    form = StudentInfo()

    if form.validate_on_submit():

        conn = connector.connect(**config)
        cursor = conn.cursor()

        gradDate = 0
        if form.expGradDate.data:
            gradDate = form.expGradDate.data

        cursor.execute(
            "UPDATE students SET fName = '{1}', mName = '{2}', lName = '{3}', suffix = '{4}', preferred = '{5}', birthday = '{6}', gender = '{7}', race = '{8}', gradeLevel = '{9}', expGradDate = '{10}', street = '{11}', city = '{12}', state = '{13}', zip = '{14}', email = '{15}', phone = '{16}', bill = '{17}', otherInfo = '{18}', expSchool = '{19}' WHERE id = '{0}'".format(
                current_user.id, form.fName.data, form.mName.data, form.lName.data, form.suffix.data,
                form.preferred.data, form.bDay.data, form.gender.data, form.race.data, form.gradeLevel.data,
                gradDate, form.street.data, form.city.data, form.state.data, form.zip.data,
                form.email.data, form.phone.data, 20, form.otherInfo.data, form.expSchool.data))

        # # Disability query
        # if form.disability.data == 'on':
        #     cursor.execute(
        #         "INSERT INTO disability (studentID, disability) VALUES ('{0}', '{1}')".format(current_user.id,
        #                                                                                       form.disabilityDesc.data))
        #
        # # Health condition query
        # if form.healthConds.data == 'on':
        #     cursor.execute(
        #         "INSERT INTO healthcondition (studentID, cond, descript) VALUES ('{0}', '{1}', '{2}')".format(
        #             current_user.id, form.healthCondsCond.data, form.healthCondsDesc.data))

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

        # School query
        id_chars = "0123456789"

        schoolID = ''
        for x in range(6):
            schoolID += random.choice(id_chars)

        cursor.execute(
            "INSERT INTO school (studentID, name, type, district, schoolID) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
                current_user.id, form.expSchool.data, form.expSchoolType.data, form.expSchoolDistrict.data,
                schoolID))

        # gt query
        cursor.execute("INSERT INTO gt (studentID, schoolID) VALUES ('{0}', '{1}')".format(current_user.id, schoolID))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Successfully activated your account!', 'success')
        return redirect(url_for('home'))

    return render_template('student_activate.html', title='Activate Account', form=form)


@app.route('/staff_activate', methods=['GET', 'POST'])
@login_required
def staff_activate():
    if current_user.category == 'Staff':

        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM staff WHERE staff.id = '{0}'".format(current_user.id))
        result = cursor.fetchone()

        if result:
            return redirect(url_for('home'))

        conn.commit()
        cursor.close()
        conn.close()

    form = StaffForm()

    if form.validate_on_submit():
        conn = connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO staff (id, fName, mName, lName, suffix, phone, email, street, city, state, zip) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')".format(
                current_user.id, form.fName.data, form.mName.data, form.lName.data, form.suffix.data, form.phone.data,
                form.email.data, form.street.data, form.city.data, form.state.data, form.zip.data))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Successfully activated your account!', 'success')
        return redirect(url_for('home'))

    return render_template('staff_activate.html', title='Activate Account', form=form)


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

        cursor.execute("SELECT curSize, price FROM class WHERE classID = '{0}'".format(class_id))
        class_info = cursor.fetchone()

        cursor.execute("SELECT bill FROM students WHERE id = '{0}'".format(current_user.id))
        bill = cursor.fetchone()

        # Increment the class' curSize
        cursor.execute("UPDATE class SET curSize = {0} WHERE classID = '{1}'".format(class_info[0] + 1, class_id))

        # Increment the student's bill
        cursor.execute(
            "UPDATE students SET bill = {0} WHERE id = '{1}'".format(bill[0] + class_info[1], current_user.id))

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
            "timeSlotID='{5}', sessionID='{6}', price='{7}' WHERE classID = '{8}'".format(
                form.title.data, form.lvl.data, form.maxCap.data, form.instructorID.data, form.room.data,
                form.timeslotID.data, form.sessionID.data, form.price.data, class_id))

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


@app.route('/roster/<class_id>', methods=['GET', 'POST'])
@login_required
def roster(class_id):
    students = None
    if current_user.category == 'Student':
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('home'))

    # Create the connection to the database
    conn = connector.connect(**config)

    # Create the cursor for the connection
    cursor = conn.cursor()

    cursor.execute("SELECT * "
                   "FROM students s, class c, takes t "
                   "WHERE s.id = t.studentID "
                   "AND c.classID = t.classID "
                   "AND c.classID = '{0}'".format(class_id))

    students = cursor.fetchall()

    # Commit the data to the database
    conn.commit()

    # Close the cursor
    cursor.close()

    # Close the connection to the database
    conn.close()

    return render_template('roster.html', title='Roster', students=students)
