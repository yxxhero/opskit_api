from flask_restful import Resource
from flask_restful import reqparse
from opskit_api.common.login_helper import checkuserpasswd
from opskit_api.common.paasswordmd5 import md5passwd  

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, location='form')
        parser.add_argument('password', type=str, required=True, location='form')
        args = parser.parse_args()
        try:
            if checkuserpasswd(args.username, md5passwd(args.password)):
                return {"code": 0}
            else:
                return {"code": 1, 'message': '用户名或密码错误!!!'}
        except Exception as e:
            return {"code": 1, 'message': str(e)}
