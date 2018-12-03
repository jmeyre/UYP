from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

""" (No need to apply online)
class ApplyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
"""


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class StudentInfo(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    mName = StringField('Middle Name', validators=[Length(min=2, max=20)])
    lName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    suffix = StringField('Suffix', validators=[Length(min=1, max=3)])
    """Might not need the length validator for DateField"""
    bDay = DateField('Birthday', format='%d/%m/%Y', validators=(DataRequired(), Length(min=8, max=10)))
    Gender = RadioField('Gender', choices=[('Male', 'Male'), ('Male', 'Male')], validators=[DataRequired()])

