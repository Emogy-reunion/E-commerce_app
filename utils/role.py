'''
This decorator checks the user roles
'''
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def role_required(role):
    '''
    role: the role required to access the route
    returns a decorator
    '''

    def decorator(func):
        '''
        func: decorated route's function
        '''
        @wraps(func) # wraps the function to maintain its documentation
        def wrapper(*args, **kwargs):
            '''
            extends the functionality of the decorated route's function
            '''
            if current_user.role != 'admin':
                '''
                check if user doesn't have admin privileges
                if true redirect them to guest_dashboard
                '''
                return redirect(url_for('dash.guest_dashboard'))
            
            # call the decorated function
            return func(*args, **kwargs)
        return wrapper
    return decorator

