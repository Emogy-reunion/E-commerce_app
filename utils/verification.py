"""
sends the verification token via email to verify the user's email
"""
from flask import url_for, render_template
from flask_mail import Mail, Message


def send_verification_email(user):
    token = user.generate_token()

    verification_url = url_for('verify.verify_email', token=token, _external=True)
    msg = Message(
            subject='Verify your email',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email]
            )
    msg.body = f"Click the following link to verify your email: {verification_url}"
    msg.html = render_template('verification.html', username=user.firstname, verification_url=verification_url)
    mail.send(msg)
