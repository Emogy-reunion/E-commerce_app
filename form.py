from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, MultipleFileField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Email, Length, Regexp, EqualTo, Optional, NumberRange

class RegistrationForm(FlaskForm):
    '''
    Represents the fields of a registration form
    '''
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[Email(), InputRequired(), Length(max=30)])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+2547\d{8}$', message="Phone number must start with +2547 followed by 8 digits.")
        ])
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
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0, message='Price must be greater than or equal to 0')])
    brand = StringField('Brand', validators=[DataRequired(), Length(max=40, message='Must not exceed 45 characters!')])
    gender = SelectField('Gender', choices=[('unisex', 'Unisex'), ('men', 'Men'), ('women', 'Women')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=330, message='Description must not exceed 330 characters!')])
    files = MultipleFileField('select images')
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    '''
    form to allow users to filter and search collections
    '''
    name = StringField('Shoe name', validators=[Optional(), Length(max=50, message='Must not exceed 50 characters!')])
    min_price = FloatField('Min_price', validators=[Optional(), NumberRange(min=0, message="Minimum price must be greater than or equal to 0")])
    max_price = FloatField('Maximum price', validators=[Optional(), NumberRange(min=0, message="Maximum price must be greater than or equal to 0")])
    brand = StringField('Brand', validators=[Optional(), Length(max=50, message='Must not exceed 50 characters!')])
    gender = SelectField('Gender', choices=[('', 'Select a gender'), ('unisex', 'Unisex'), ('men', 'Men'), ('women', 'Women')], validators=[Optional()])
    submit = SubmitField('Search')

class UpdateUpload(FlaskForm):
    '''
    form to allow users to update the sneakers
    '''
    name = StringField('Shoe name', validators=[DataRequired(), Length(max=45, message='Must not exceed 45 characters!')])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0, message="Price must be greater than or equal to 0")])
    brand = StringField('Brand', validators=[DataRequired(), Length(max=45, message='Must not exceed 45 characters!')])
    gender = SelectField('Gender', choices=[('unisex', 'Unisex'), ('men', 'Men'), ('women', 'Women')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=330, message='Description must not exceed 330 characters!')])
    submit = SubmitField('Update')

class QuantityForm(FlaskForm):
    '''
    form to allow users to increment or decrement the quantity of items
    '''
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, message="Price must be greater than or equal to 1")])

class SizeForm(FlaskForm):
    '''
    form to allow users to select the size
    '''
    size = SelectField('Select Size', choices=[(str(i), str(i)) for i in range(36, 46)])

class CheckoutForm(FlaskForm):
    '''
    allows users to enter checkout details
    '''
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+2547\d{8}$', message="Phone number must start with +2547 followed by 8 digits.")
        ])
    submit = SubmitField('Order now')
