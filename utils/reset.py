'''
sends a password reset email
'''
from flask import url_for, render_template
from utils.verification import mail
from flask_mail import Message


def send_reset_email(user):
    token = user.generate_token()

    verifcation_url = url_for('reset.reset_password', token=token, _external=True)
    msg = Message(
            subject='Reset password request',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to reset your password: {verification_url}'
    msg.html = render_template('reset.html', verification_url=verification_url, username=user.firstname)
    mail.send(msg)
