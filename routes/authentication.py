from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from form import RegistrationForm, LoginForm
from model import db, Users
from utils.verification import send_verification_email
from flask_login import login_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.form)

        if form.validate_on_submit():
            email = form.email.data.lower()
            password = form.password.data
            remember = form.remember.data

            user = User.query.filter_by(email=email).first()

            if user:
                if user.verified:
                    if user.check_password(password):
                        login_user(user, remember=remember)
                        return jsonify({'success': 'Successfully logged in'})
                    else:
                        return jsonify({'error': 'Incorrect password. Please try again!'})
                else:
                    return jsonify({'verify': 'Verify you email address to continue'})
            else:
                return jsonify({'error': 'Incorrect email. Please try again!'})
        else:
            return jsonify({'errors': form.errors})
    return render_template('login.html', form=form)



@auth.route('/register', methods=['GET', 'POST'])
def register():
     
    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        form = RegistrationForm(request.form)

        if form.validate_on_submit():
            '''
            checks if form fields are valid
            extracts the form data
            '''
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data.lower()
            password = form.password.data
            
            # check if the user exists
            user = Users.query.filter_by(email=email).first()

            if user:
                return jsonify({'error': 'An account with this email already exists. Please login or use a different email'})
            else:
                try:
                    new_user = Users(firstname=firstname, lastname=lastname, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    send_verification_email(new_user)
                    return jsonify({'success': 'Account created succesfully!. A verification email has been sent!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occured. Please try again!'})
        else:
            return jsonify({'errors': form.errors})

