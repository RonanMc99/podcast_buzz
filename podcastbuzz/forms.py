from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LogonForm(FlaskForm):
    '''Log on to the app'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    '''Register for the app'''
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=25)])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat Password',[DataRequired(),EqualTo('password', message='Passwords do not match')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
