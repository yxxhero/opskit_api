from flask_restful import Resource
from flask_restful import reqparse
from flask import request, g
from opskit_api.common.login_helper import auth_decorator
from opskit_api.common.login_helper import jwt_decode_token


class Essay(Resource):

    method_decorators = {'post': [auth_decorator]}
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)
    

    def get(self):
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('page_size', type=int, default=10)
        self.parser.add_argument('username', type=str)
        return {'code': 200, 'msg': "请求成功", 'data': []}

    def post(self):
        self.parser.add_argument('title', type=str, required=True)
        self.parser.add_argument('content', type=str, required=True)
        return {'code': 200, 'msg': "请求成功", 'data': []}
