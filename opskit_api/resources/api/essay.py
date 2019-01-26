from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from opskit_api.models import Note, User
from opskit_api.common.login_helper import auth_decorator
from opskit_api.common.login_helper import jwt_decode_token


class Essay(Resource):

    method_decorators = {'post': [auth_decorator]}

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('page', type=int, default=1, location='args')
        self.parser.add_argument(
            'page_size', type=int, default=10, location='args')
        self.parser.add_argument('username', type=str,
                                 default="all", location='args')
        self.parser.add_argument('note_type', type=str,
                                 default="web", location='args')
        args = self.parser.parse_args()
        print(args)
        try:
            note_list = Note.query.limit(args.page_size).offset(args.page_size * (args.page - 1)).all()
        except Exception as e:
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': []}
            

    def post(self):
        self.parser.add_argument(
            'title', type=str, required=True, location='json')
        self.parser.add_argument(
            'content', type=str, required=True, location='json')
        self.parser.add_argument(
            'note_type', type=str, required=True, location='json')
        username = jwt_decode_token(request.headers.get('Authorization'))['data']['username']
        try:
            user = User.query.filter(user_name=username).first()  
            Note(title=args.title, content=args.content, note_type=args.note_type, user=user).save()
        except Exception as e:
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "提交成功"}


         

        return {'code': 200, 'msg': "请求成功", 'data': []}
