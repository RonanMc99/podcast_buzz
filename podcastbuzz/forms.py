from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LogonForm(FlaskForm):
    '''Log on to the app'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    '''Register for the app'''
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirmpassword = PasswordField('Repeat Password',[DataRequired(), EqualTo('password', message='Passwords do not match')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
