from flask_restful import Resource
from flask_restful import reqparse

class Login(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True) 
        args = parser.parse_args()
        try:
            pass
        except Exception as e:
            return {"code": 1}
        else:
            return {"code": 0}
