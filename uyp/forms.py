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
    submit = SubmitField('Save Changes')


"""need to generate a classID"""


class AddClassForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    lvl = RadioField('Course Level', choices=[('4th - 5th', '4th - 5th'), ('6th - 8th', '6th - 8th'), ('9th - 12th', '9th - 12th')], validators=[DataRequired()])
    maxCap = IntegerField('Maximum Capacity', validators=[DataRequired()])
    instructorID = StringField('Instructor ID', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    timeslotID = StringField('Choose a Time Slot', validators=[(DataRequired())])
    sessionID = StringField('Choose a Session', validators=[DataRequired()])
    price = IntegerField('Price (in dollars)', validators=[DataRequired()])
    submit = SubmitField('Add Class')


class StudentInfo(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired()])
    mName = StringField('Middle Name', validators=[Optional()])
    lName = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', validators=[Optional()])
    preferred = StringField('Preferred Name', validators=[Optional()])
    bDay = DateField('Birthday', validators=[Optional()], format='%Y-%m-%d')
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    race = RadioField('Race',
                      choices=[('White', 'Caucasian'), ('Black', 'African American'), ('Native', 'Native American'),
                               ('Islander', 'Pacific Islander'),
                               ('Asian', 'Asian'), ('Indian', 'Indian')], validators=[Optional()])
    gradeLevel = StringField('Grade Level', validators=[Optional()])
    expGradYear = DateField('Expected Graduation Year', validators=[Optional()], format='%Y-%m-%d')
    #expHighSchool = StringField('Expected High School', validators=[Optional()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired(), Length(min=5, max=5, message='Please enter a 5 digit zip code')])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=10, max=10, message='Please enter a 10 digit phone number')])
    #siblings = StringField('Sibling IDs', validators=[Optional()])
    disability = StringField('Disabilities?', validators=[Optional()])
    disabilityDesc = StringField('Describe disability', validators=[Optional()])
    healthConds = StringField('Health Conditions?', validators=[Optional()])
    healthCondsCond = StringField('What is the condition?', validators=[Optional()])
    healthCondsDesc = StringField('Describe health condition', validators=[Optional()])
    ESL = RadioField('English Second Language?', choices=[('1', 'Yes'), ('0', 'No')], validators=[Optional()])
    GT = RadioField('GT?', choices=[('1', 'Yes'), ('0', 'No')], validators=[Optional()])
    submit = SubmitField('Submit Info')


class DisabilityForm(FlaskForm):
    type = StringField('Form of disability', validator=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Save Changes')


class HealthConditionForm(FlaskForm):
    cond = StringField('Health Condition', validator=[DataRequired(), Length(min=2, max=20)])
    desc = StringField('Description', validator=[DataRequired(), Length(min=2, max=200)])


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
