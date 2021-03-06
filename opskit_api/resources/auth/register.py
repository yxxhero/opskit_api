from flask_restful import Resource
from flask_restful import reqparse
from opskit_api.common.paasswordmd5 import md5passwd
from opskit_api.common.login_helper import checkuserexist
from opskit_api.models import User


class Register(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.parser.add_argument("username", type=str, required=True, location="json")
        self.parser.add_argument("password", type=str, required=True, location="json")
        self.parser.add_argument("email", type=str, required=True, location="json")
        args = self.parser.parse_args()
        try:
            if checkuserexist(args.username):
                return {"code": 1, "msg": "用户名已经存在"}
            user = User(
                user_name=args.username,
                user_password=md5passwd(args.password),
                user_email=args.email,
            )
            user.save()
        except Exception as e:
            return {"code": 1, "msg": str(e)}
        else:
            return {"code": 0, "msg": "注册成功"}
