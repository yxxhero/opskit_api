from flask_restful import Resource
from flask_restful import reqparse
from opskit_api.common.paasswordmd5 import md5passwd
from opskit_api.models import User, db

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user', type=str, required=True, location='form') 
        parser.add_argument('password', type=str, required=True, location='form') 
        parser.add_argument('email', type=str, required=True, location='form') 
        args = parser.parse_args()
        try:
            user = User(user_name=args.user, user_password=md5passwd(args.password), user_email=args.email)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return {"code": 1, 'message': str(e)}
        else:
            return {"code": 0, 'message': '注册成功'}
