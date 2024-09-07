"""
sends a verification email
"""
def send_verification_email(user):
    token = user.generate_token()

    verification_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message(
            subject='Verify your email',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to verify your email address: {verification_url}'
    msg.html = render_template('verification.html', verification_url=verification_url, username=user.firstname)
    mail.send(msg
