from flask_restful import Resource
from flask import current_app
import traceback
from flask_restful import reqparse
from opskit_api.common.login_helper import checkuserpasswd
from opskit_api.common.login_helper import checkuserexist
from opskit_api.common.login_helper import jwt_encode_token
from opskit_api.common.paasswordmd5 import md5passwd
from opskit_api.models import redis_store, User


class Login(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.parser.add_argument("username", type=str, required=True, location="json")
        self.parser.add_argument("password", type=str, required=True, location="json")
        args = self.parser.parse_args()
        try:
            if not checkuserexist(args.username):
                return {"code": 1, "msg": "用户名不存在!!!"}

            if checkuserpasswd(args.username, md5passwd(args.password)):
                userrole = (
                    User.query.filter_by(user_name=args.username)
                    .first()
                    .user_role.value
                )
                authtoken = jwt_encode_token(args.username)
                redis_store.set(
                    args.username,
                    authtoken,
                    current_app.config.get("TOKEN_DEADLINE", 60),
                )
                return {
                    "code": 0,
                    "token": authtoken,
                    "username": args.username,
                    "userrole": userrole,
                }
            else:
                return {"code": 1, "msg": "用户名或密码错误!!!"}
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {"code": 1, "msg": str(e)}
