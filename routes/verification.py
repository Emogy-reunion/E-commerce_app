"""
contains routes that handle user verification
"""
from flask import Blueprint, render_template, url_for, redirect, request, flash
from model import Users, db
from form import ReverificationForm
from utils.verification import send_verification_email


verify = Blueprint('verify', __name__)


@verify.route('/verify_email/<token>')
def verify_email(token):
    user = Users.verify_token(token)

    if user:
        user.verified = True
        db.session.commit()
        return render_template('success.html')
    else:
        flash('The verification link has expired or is invalid. Try again', 'danger')
        return redirect(url_for('verify.resend_verification_email'))


@verify.route('/resend_verification_email', methods=['GET', 'POST'])
def resend_verification_email():
    '''
    reverifies the user's email
    renders the template where user's enter their email to get a reverification email
    '''
    form = ReverificationForm()

    if request.method == 'GET':
        return render_template('reverification.html', form=form)
    else:
        if form.validate_on_submit():
            email = form.email.data.lower()

            user = Users.query.filter_by(email_email).first()
            if user:
                if user.verified:
                    flash('Already verified. Please login!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    send_verification_email(user)
                    flash('A new verification email has been sent', 'success')
                    return redirect(request.url)
            else:
                flash('Incorrect email. Please try again!', 'error')
                return redirect(request.url)

