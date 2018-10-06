from flask_restful import Resource
from flask_restful import reqparse
from opskit_api.common.login_helper import checkuserpasswd
from opskit_api.common.login_helper import jwt_encode_token 
from opskit_api.common.paasswordmd5 import md5passwd  
from opskit_api.models import redis_store 

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, location='form')
        parser.add_argument('password', type=str, required=True, location='form')
        args = parser.parse_args()
        try:
            if checkuserpasswd(args.username, md5passwd(args.password)):
                authtoken = jwt_encode_token(args.username)
                redis_store.set(args.username, authtoken)
                return {"code": 0, 'token': authtoken}
            else:
                return {"code": 1, 'message': '用户名或密码错误!!!'}
        except Exception as e:
            # raise e
            return {"code": 1, 'message': str(e)}
