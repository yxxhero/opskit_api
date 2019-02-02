from flask_restful import Resource
from flask_restful import reqparse
from flask import g, current_app
from opskit_api.models import Note, User
import traceback
from opskit_api.common.login_helper import auth_decorator


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
                                 default=None, location='args')
        self.parser.add_argument('note_type', type=str,
                                 default=None, location='args')
        args = self.parser.parse_args()
        try:
            note_list = Note.query.limit(args.page_size).offset(
                args.page_size * (args.page - 1)).all()
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': [{'content': item.content, 'note_type': item.note_type.value} for item in note_list]}

    def post(self):
        self.parser.add_argument(
            'title', type=str, required=True, location='json')
        self.parser.add_argument(
            'content', type=str, required=True, location='json')
        self.parser.add_argument(
            'raw_content', type=str, required=True, location='json')
        self.parser.add_argument(
            'note_type', type=int, required=True, location='json')
        args = self.parser.parse_args()
        username = g.username
        try:
            user = User.query.filter_by(user_name=username).first()
            args.user = user
            Note(**args).save()
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "提交成功"}
