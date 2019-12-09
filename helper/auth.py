from flask import request

def get_current_user():
    current_user = request.cookies.get('user_name')
    if current_user:
        return current_user
    return None