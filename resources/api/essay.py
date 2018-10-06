from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from opskit_api.common.login_helper import auth_decorator 
from opskit_api.common.login_helper import jwt_decode_token 

class Essay(Resource):

    method_decorators = {'post': [auth_decorator]}
    
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('page_size', type=int, default=10) 
        parser.add_argument('username', type=str) 
        print(parser.parse_args())
        return {'code': 200, 'msg': "请求成功", 'data': []}

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('content', type=str, required=True) 
        print(parser.parse_args())
        print(jwt_decode_token(request.headers['Authorization']))
        return {'code': 200, 'msg': "请求成功", 'data': []}
