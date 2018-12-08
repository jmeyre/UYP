from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectMultipleField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=255,
                                                                    message='Titles are at least 2 characters long')])
    lvl = RadioField('Course Level', choices=[('one', '4th - 5th'), ('two', '6th - 8th'), ('three', '9th - 12th')],
                     validators=[DataRequired()])
    maxCap = IntegerField('Maximum Capacity', validators=[DataRequired()])
    instructorID = StringField('Instructor ID',
                               validators=[DataRequired(), Length(min=6, max=6, message='User IDs are 6 characters')])
    room = StringField('Room', validators=[DataRequired(), Length(min=2, max=255)])
    timeslotID = RadioField('Time Slot', choices=[('1', '9:45 - 11:15'), ('2', 'Lunch and Recreation'),
                                                  ('3', '1:15 - 2:45')], validators=[(DataRequired())])
    sessionID = RadioField('Session', choices=[('one', 'Week 1'), ('two', 'Week 2'), ('three', 'Week 3')],
                           validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Class')


class StudentInfo(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    mName = StringField('Middle Name', validators=[Length(min=2, max=20)])
    lName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    suffix = StringField('Suffix', validators=[Length(min=1, max=3)])
    """Might not need the length validator for DateField"""
    bDay = DateField('Birthday', format='%d/%m/%Y', validators=[(DataRequired(), Length(min=8, max=10))])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Male', 'Male')], validators=[DataRequired()])
    race = SelectMultipleField('Race',
                               choices=[('Caucasian', 'White'), ('African American', 'Black'),
                                        ('Native American', 'Native')
                                   , ('Pacific Islander', 'Islander'), ('Asian', 'Asian'), ('Indian', 'Indian')])
    expGradDate = DateField('Expected Graduation Date', format='%m/%Y',
                            validators=[DataRequired(), Length(min=6, max=7)])
    expHighSchool = StringField('Expected High School')
    street = StringField('Street', validators=[DataRequired(), Length(min=2, max=20)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=20)])
    zip = IntegerField('Zip', validators=[DataRequired(), Length(min=5, max=9)])
    email = StringField('Email')
    phone = StringField('Phone Number')
    siblings = StringField('Sibling IDs', validators=[Length(min=1, max=50)])
    disability = RadioField('Disabilities?', choices=[('Yes', 'yes'), ('No', 'no')])
    healthConds = RadioField('Health Conditions?', choices=[('Yes', 'yes'), ('No', 'no')])
    ESL = RadioField('English Second Language', choices=[('Yes', 'yes'), ('No', 'no')])
    GT = RadioField('GT?', choices=[('Yes', 'yes'), ('No', 'no')])
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
    """Html 5 fores the format %Y-%m-%d"""
    startDate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    endDate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Session')