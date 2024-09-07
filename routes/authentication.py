from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from form import RegistrationForm
from model import db, Users
from utils.verification import send_verification_email

auth = Blueprint('auth', __name__)

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
            email = form.email.data
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


