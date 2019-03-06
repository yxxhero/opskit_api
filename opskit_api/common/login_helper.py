from opskit_api.models import User, app, redis_store
from flask import request, g, current_app
from functools import wraps
import time
import datetime
import traceback
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt


def checkuserpasswd(username, password):
    if User.query.filter_by(user_name=username, user_password=password).count():
        return True
    else:
        return False


def checkuserexist(username):
    if User.query.filter_by(user_name=username).count():
        return True
    else:
        return False


def jwt_encode_token(username):
    login_time = time.time()
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=app.config.get('TOKEN_DEADLINE', 60)),
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
        app.config['SECRET_KEY']
    )


def auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {'code': 401, 'message': '未认证'}, 401
        else:
            try:
                username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
                if redis_store.get(username).decode('utf-8') != request.headers.get('Authorization'):
                    return {'code': 401, 'message': 'token失效'}, 401
                else:
                    g.username = username
                    return func(*args, **kwargs)
            except ExpiredSignatureError:
                current_app.logger.error(traceback.format_exc())
                return {'code': 401, 'message': 'token已过期'}, 401
            except InvalidTokenError:
                current_app.logger.error(traceback.format_exc())
                return {'code': 401, 'message': 'token不可用'}, 401
            except Exception as e:
                current_app.logger.error(traceback.format_exc())
                return {'code': 401, 'message': 'token解析异常', 'data': str(e)}, 401
    return wrapper


def common_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            g.username = None
        else:
            try:
                username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
                if redis_store.get(username).decode('utf-8') != request.headers.get('Authorization'):
                    g.username = None
                else:
                    g.username = username
            except Exception:
                g.username = None
        return func(*args, **kwargs)
    return wrapper
