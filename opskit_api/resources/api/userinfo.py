from flask_restful import Resource, reqparse
from flask import g, current_app
from opskit_api.models import User
import traceback
from opskit_api.common.login_helper import auth_decorator


class UserInfo(Resource):

    method_decorators = {'put': [auth_decorator]}

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):

        try:
            username = g.username
            user_ins = User.query.filter_by(user_name=username).first()
            if user_ins:
                user_info = {
                    "username": user_ins.user_name,
                    "userrole": user_ins.user_role.value,
                    "useremail": user_ins.user_email,
                    "userauditing": user_ins.is_auditing,
                    "useravatar": user_ins.user_avatar,
                    "userdescription": user_ins.user_description,
                    "createtime": user_ins.create_time,
                    "notecount": user_ins.note_set.count()
                }
            else:
                return {'code': 1, 'msg': "无法找到用户信息"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取用户信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': user_info}

    def put(self):

        self.parser.add_argument(
            'useremail', type=str, required=True, location='json')
        self.parser.add_argument(
            'userdescription', type=str, required=True, location='json')
        args = self.parser.parse_args()
        try:
            username = g.username
            user_ins = User.query.filter_by(user_name=username).first()
            if user_ins:
                user_ins.user_email = args.useremail
                user_ins.user_description = args.userdescription
                user_ins.update()
            else:
                return {'code': 1, 'msg': "无法找到用户信息"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '更新用户信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功"}
