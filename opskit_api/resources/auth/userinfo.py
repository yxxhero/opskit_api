import traceback
from flask_restful import Resource
from flask import g, current_app
from opskit_api.common.login_helper import userinfo_decorator


class UserInfo(Resource):

    method_decorators = [userinfo_decorator]

    def get(self):
        try:
            username = g.username
            return {"code": 0, "username": username}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {"code": 401, "msg": "认证信息错误"}
