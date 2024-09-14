'''
This module handles user password reset
'''
from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify
from model import Users, db
from utils.reset import send_reset_email
from form import ForgotPassword, ResetForm


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
        return redirect(url_for('reset.input_password', user_id=user.id))
    else:
        flash('The verification token is invalid or has expired!', 'danger')
        return redirect(url_for('reset.forgot_password'))

@reset.route('/input_password/<int:user_id>', methods=['GET', 'POST'])
def input_password(user_id):
    form = ResetForm()

    if request.method == 'POST':
        form = ResetForm(request.form)

        if form.validate_on_submit():
            password = form.password.data

            user = db.session.get(Users, user_id)
            try:
                user.set_password(password)
                db.session.commit()
                return jsonify({'success': 'Password updated successfully!'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured, try again!'})
        else:
            return jsonify({'errors': form.errors})
    return render_template('password.html', form=form, user_id=user_id)
