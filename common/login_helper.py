from opskit_api.models import User, app, redis_store
from flask import request, g
from functools import wraps
import time, datetime 
import jwt

def checkuserpasswd(username, password):
    if User.query.filter_by(user_name=username, user_password=password).count():
        return True
    else:
        return False

def jwt_encode_token(username):
    login_time = time.time()
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
        'iat': datetime.datetime.utcnow(),
        'iss': 'ken',
        'data': {
            'username': username,
            'login_time': login_time
        }
    }
    return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            ).decode('utf-8')

def jwt_decode_token(jwttoken):
    return jwt.decode(
                jwttoken,
                app.config['SECRET_KEY'],
                options={'verify_exp': False}
            )

def auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {'code': 403, 'message': '未认证'}, 403 
        else:
            try:
                username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
                if redis_store.get(username).decode('utf-8') != request.headers.get('Authorization'):
                    return {'code': 403, 'message': 'token失效'}, 403
                else:
                    g.username = username
                    return func(*args, **kwargs)
            except Exception as e:
                return {'code': 403, 'message': 'token解析异常', 'data': str(e)}, 403
    return wrapper

