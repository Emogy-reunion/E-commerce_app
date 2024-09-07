"""
contains routes that handle user verification
"""
from flask import Blueprint, render_template, url_for, redirect
from model import Users, db


verify = Blueprint('verify', __name__)


@verify.route('/verify_email/<token>')
def verify_email(token):
    user = Users.verify_token(toke)

    if user:
        user.verified = True
        db.session.commit()
        return render_template('success.html')
    else:
        flash('The verification link has expired or is invalid. Try again', 'danger')
        return redirect(url_for('verify.resend_verification_email'))

