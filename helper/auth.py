from flask import request

def is_authenticated():
    current_user = request.cookies.get('user_name')
    if current_user:
        return True
    return False