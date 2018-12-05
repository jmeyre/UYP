from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectMultipleField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ApplyForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    category = RadioField('Account Category', choices=[('Student', 'Student'), ('Staff', 'Staff')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    user_id = IntegerField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountForm(FlaskForm):
    submit = SubmitField('Save Changes')


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
    submit = SubmitField('Save Changes')


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

