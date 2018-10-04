from flask_restful import Resource
from flask_restful import reqparse

class HelloWorld(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('foo', type=int, required=True)
        parser.add_argument('bar', type=int, required=True) 
        print(parser.parse_args())
        return {'code': 200, 'msg': "请求成功", 'data': []}
