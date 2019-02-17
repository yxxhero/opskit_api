from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app
from opskit_api.models import Note
import traceback


class Essays(Resource):

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
            note_list = Note.query.order_by(Note.create_time.desc()).limit(args.page_size).offset(
                args.page_size * (args.page - 1)).all()
            note_infos = [{'view_count': item.view_count, 'href': '/essay/view/?note_id=' + str(item.id), 'content': item.content, 'note_type': item.note_type.value, 'raw_content': item.raw_content, 'title': item.title, 'username': item.user.user_name, 'useravatar': item.user.user_avatar} for item in note_list]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': note_infos}
