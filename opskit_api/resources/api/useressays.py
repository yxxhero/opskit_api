from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app, g
from opskit_api.models import Note, User
from opskit_api.common.login_helper import auth_decorator
import traceback


class UserEssays(Resource):

    method_decorators = [auth_decorator]

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('page', type=int, default=1, location='args')
        self.parser.add_argument(
            'page_size', type=int, default=10, location='args')
        args = self.parser.parse_args()
        username = g.username
        try:
            user = User.query.filter_by(user_name=username).first()
            usernotetotal = Note.query.filter_by(user=user).count()
            note_list = Note.query.filter_by(user=user).order_by(Note.create_time.desc()).limit(args.page_size).offset(
                args.page_size * (args.page - 1)).all()
            note_infos = [{'update_time': item.update_time, 'view_count': item.view_count, 'href': '/essay/view/?note_id=' + str(
                item.id), 'content': item.content, 'note_type': item.note_type.value, 'raw_content': item.raw_content, 'title': item.title, 'username': item.user.user_name, 'useravatar': item.user.user_avatar} for item in note_list]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': {'usernotelist': note_infos, 'usernotetotal': usernotetotal}}
