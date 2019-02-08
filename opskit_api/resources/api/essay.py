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
        self.parser.add_argument('id', type=str,
                                 default=None, location='args')
        args = self.parser.parse_args()
        try:
            note_ins = Note.query.filter_by(id=args.id).first()
            if note_ins:
                note_info = {
                    "title": note_ins.title,
                    "content": note_ins.content,
                    "raw_content": note_ins.raw_content,
                    "username": note_ins.user.user_name,
                    "useravatar": note_ins.user.user_avatar,
                    "createtime": note_ins.create_time,
                    "updatetime": note_ins.update_time
                }
            else:
                return {'code': 1, 'msg': "文章不存在"}
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取文章信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': note_info}

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
