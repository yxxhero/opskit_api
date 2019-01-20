from flask_restful import Resource
from flask_restful import reqparse
from opskit_api.common.login_helper import checkuserpasswd
from opskit_api.common.login_helper import checkuserexist
from opskit_api.common.login_helper import jwt_encode_token
from opskit_api.common.paasswordmd5 import md5passwd
from opskit_api.models import redis_store, app


class Login(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.parser.add_argument('username', type=str,
                                 required=True, location='json')
        self.parser.add_argument('password', type=str,
                                 required=True, location='json')
        args = self.parser.parse_args()
        try:
            if not checkuserexist(args.username):
                return {"code": 1, 'message': '用户名不存在!!!'}

            if checkuserpasswd(args.username, md5passwd(args.password)):
                authtoken = jwt_encode_token(args.username)
                redis_store.set(args.username, authtoken,
                                app.config.get('TOKEN_DEADLINE', 60))
                return {"code": 0, 'token': authtoken, 'username': args.username}
            else:
                return {"code": 1, 'message': '用户名或密码错误!!!'}
        except Exception as e:
            return {"code": 1, 'message': str(e)}
