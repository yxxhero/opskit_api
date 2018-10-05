from opskit_api.models import User

def checkuserpasswd(username, password):
    if User.query.filter_by(user_name=username, user_password=password).count():
        return True
    else:
        return False
