from flask_restful import Resource, reqparse
from flask import request
from opskit_api.common.login_helper import jwt_decode_token
from opskit_api.models import redis_store


class Logout(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('username', type=str,
                                 required=True, location='args')
        args = self.parser.parse_args()
        try:
            username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
            if args.username == username:
                redis_store.delete(username)
            else:
                return {"code": 1, 'msg': '用户名和Token不匹配'}
        except Exception as e:
            redis_store.delete(args.username)
            return {"code": 0, 'msg': str(e)}
        else:
            return {"code": 0, 'msg': '注销成功'}
