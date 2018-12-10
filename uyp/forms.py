from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectMultipleField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from datetime import datetime


class CreateAccountForm(FlaskForm):
    # user_id = IntegerField('User ID', validators=[DataRequired()])
    category = RadioField('Account Category', choices=[('Student', 'Student'), ('Staff', 'Staff')],
                          validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # fname = StringField('First Name', validators=[DataRequired()])
    # lname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    user_id = StringField('User ID',
                          validators=[DataRequired(), Length(min=6, max=6, message='User IDs are 6 characters')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Retype New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Change Password')


class AddClassForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    lvl = StringField('Course Level', validators=[DataRequired()])
    maxCap = IntegerField('Maximum Capacity', validators=[DataRequired()])
    instructorID = StringField('Instructor ID', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    timeslotID = StringField('Choose a Time Slot', validators=[(DataRequired())])
    sessionID = StringField('Choose a Session', validators=[DataRequired()])
    price = IntegerField('Price (in dollars)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StudentInfo(FlaskForm):
    fName = StringField('First Name*', validators=[DataRequired()])
    mName = StringField('Middle Name', validators=[Optional()])
    lName = StringField('Last Name*', validators=[DataRequired()])
    suffix = StringField('Suffix', validators=[Optional()])
    preferred = StringField('Preferred Name', validators=[Optional()])
    email = StringField('Student Email', validators=[Optional(), Email()])
    phone = StringField('Student Phone Number', validators=[Optional(), Length(min=10, max=10, message='Please enter a 10 digit phone number')])
    bDay = DateField('Birthday*', validators=[DataRequired()], format='%Y-%m-%d')
    gender = StringField('Gender*', validators=[DataRequired()])
    race = StringField('Race', validators=[Optional()])
    otherInfo = StringField('Important Information about Student', validators=[Optional()])

    gradeLevel = StringField('Grade Level', validators=[DataRequired()])
    expSchool = StringField('Expected High School*', validators=[DataRequired()])
    expSchoolType = StringField('High School Type*', validators=[DataRequired()])
    expSchoolDistrict = StringField('High School District*', validators=[DataRequired()])
    expGradDate = DateField('Expected Graduation Date', validators=[Optional()], format='%Y-%m-%d')

    street = StringField('Street*', validators=[DataRequired()])
    city = StringField('City*', validators=[DataRequired()])
    state = StringField('State*', validators=[DataRequired()])
    zip = StringField('Zip*', validators=[DataRequired(), Length(min=5, max=5, message='Please enter a 5 digit zip code')])

    disability = StringField('Disabilities?', validators=[Optional()])
    disabilityDesc = StringField('Describe disability', validators=[Optional()])

    healthConds = StringField('Health Conditions?', validators=[Optional()])
    healthCondsCond = StringField('What is the condition?', validators=[Optional()])
    healthCondsDesc = StringField('Describe health condition', validators=[Optional()])

    ESL = StringField('English Second Language?', validators=[Optional()])
    GT = StringField('GT?', validators=[Optional()])

    guardian1_fName = StringField('Guardian First Name*', validators=[DataRequired()])
    guardian1_mName = StringField('Guardian Middle Name', validators=[Optional()])
    guardian1_lName = StringField('Guardian Last Name*', validators=[DataRequired()])
    guardian1_phone = StringField('Guardian Phone Number*', validators=[DataRequired()])
    guardian1_email = StringField('Guardian Email*', validators=[DataRequired(), Email()])
    guardian1_street = StringField('Guardian Street*', validators=[DataRequired()])
    guardian1_city = StringField('Guardian City*', validators=[DataRequired()])
    guardian1_state = StringField('Guardian State*', validators=[DataRequired()])
    guardian1_zip = StringField('Guardian Zip*', validators=[DataRequired()])

    guardian2_prompt = StringField('Add a 2nd guardian?', validators=[Optional()])
    guardian2_fName = StringField('Guardian First Name', validators=[Optional()])
    guardian2_mName = StringField('Guardian Middle Name', validators=[Optional()])
    guardian2_lName = StringField('Guardian Last Name', validators=[Optional()])
    guardian2_phone = StringField('Guardian Phone Number', validators=[Optional()])
    guardian2_email = StringField('Guardian Email', validators=[Optional(), Email()])
    guardian2_street = StringField('Street', validators=[Optional()])
    guardian2_city = StringField('City', validators=[Optional()])
    guardian2_state = StringField('Street', validators=[Optional()])
    guardian2_zip = StringField('Zip', validators=[Optional()])

    submit = SubmitField('Submit Info')


class StaffForm(FlaskForm):
    fName = StringField('First Name*', validators=[DataRequired()])
    mName = StringField('Middle Name', validators=[Optional()])
    lName = StringField('Last Name*', validators=[DataRequired()])
    suffix = StringField('Suffix', validators=[Optional()])
    phone = StringField('Phone Number*', validators=[DataRequired()])
    email = StringField('Email*', validators=[Email(), DataRequired()])
    street = StringField('Street*', validators=[DataRequired()])
    city = StringField('City*', validators=[DataRequired()])
    state = StringField('State*', validators=[DataRequired()])
    zip = IntegerField('Zip*', validators=[DataRequired()])

    submit = SubmitField('Submit')


class SiblingForm(FlaskForm):
    siblingID = StringField('Sibling ID', validators=[DataRequired()])
    submit = SubmitField('Add Sibling')


class GuardianForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    mName = StringField('Middle Name', validators=[Length(min=2, max=20)])
    lName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    suffix = StringField('Suffix', validators=[Length(min=1, max=3)])
    phone = StringField('Phone Number')
    email = StringField('Email')
    street = StringField('Street', validators=[DataRequired(), Length(min=2, max=20)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=20)])
    zip = IntegerField('Zip', validators=[DataRequired(), Length(min=5, max=9)])


class SchoolForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    type = RadioField('Type', choices=[('Public', 'public'), ('Private', 'private'), ('Home', 'home')])
    district = StringField('District', validators=[Length(min=2, max=20)])


class StudentSearchForm(FlaskForm):
    search = StringField('Find Student...')


class CreateSessionForm(FlaskForm):
    # Html 5 forces the format %Y-%m-%d
    startDate = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    endDate = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_date(self):
        a = self.startDate.data
        b = self.endDate.data
        if a > b:
            raise ValidationError('Start Date is before End Date')
        else:
            return True
