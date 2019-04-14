from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app
from opskit_api.models import Note
import traceback


class EssayUserInfo(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('id', type=str, required=True, location='args')
        args = self.parser.parse_args()
        try:
            note_ins = Note.query.filter_by(id=args.id).first()
            if note_ins:
                user_info = {
                    "username": note_ins.user.user_name,
                    "userrole": note_ins.user.user_role.value,
                    "useremail": note_ins.user.user_email,
                    "userauditing": note_ins.user.is_auditing,
                    "useravatar": note_ins.user.user_avatar,
                    "userdescription": note_ins.user.user_description,
                    "createtime": note_ins.user.create_time,
                    "notecount": note_ins.user.note_set.count()
                }
            else:
                return {'code': 1, 'msg': "文章不存在"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取文章作者信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': user_info}

