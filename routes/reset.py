'''
This module handles user password reset
'''
from flask import Blueprint, render_template, redirect, request, flash, url_for
from model import Users, db
from utils.reset import send_reset_email


reset = Blueprint('reset', __name__)

@reset.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    
    form = ForgotPassword()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data.lower()

            user = Users.query.filter_by(email=email).first()

            if user:
                send_reset_email(user)
                flash('A password reset email has been sent!', 'success')
                return redirect(request.url)
            else:
                flash('Account not found. Please try again!', 'danger')
                return redirect(request.url)
    return render_template('forgot.html', form=form)

@reset.route('/reset_password/<token>')
def reset_password(token):
    user = Users.verify_token(token)

    if user:
        return redirect(url_for('verify.input_password', user_id=user.id))
    else:
        flash('The verification token is invalid or has expired!', 'danger')
        return redirect(url_for('verify.forgot_password'))
