from flask_restful import Resource
from flask import request
from opskit_api.common.login_helper import jwt_decode_token 
from opskit_api.models import redis_store 

class Logout(Resource):
    def get(self):
        try:
            username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
            redis_store.delete(username)
        except Exception as e:
            return {"code": 1, 'message': str(e)}
        else:
            return {"code": 0, 'message': '注销成功'}

