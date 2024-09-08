from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, Regexp, EqualTo

class RegistrationForm(FlaskForm):
    '''
    Represents the fields of a registration form
    '''
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[Email(), InputRequired(), Length(max=30)])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    showpassword = BooleanField('Show passwords')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    '''
    represents the login form fields
    '''
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    showpassword = BooleanField('Show password')
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class ReverificationForm(FlaskForm):
    '''
    represents the reverification form fields
    '''
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')


class ForgotPassword(FlaskForm):
    '''
    form where user email is collected so as to change the password
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class ResetForm(FlaskForm):
    '''
    form to collect user's new passwords
    '''

    password = PasswordField('Password', validators=[
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    showpassword = BooleanField('Show passwords')
    submit = SubmitField('Reset password')


class UploadForm(FlaskForm):
    '''
    form to collect sneaker data and upload it to server
    '''
    
    name = StringField('Shoe name', validators=[DataRequired(), Length(max=45, message='Name must not exceed 45 characters!')])
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=330, message='Description must not exceed 330 characters!')])
    files = MultipleFileField('select images')
    submit = SubmitField('Upload')
