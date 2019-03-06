from flask_restful import Resource, reqparse
from flask import g, current_app
from opskit_api.models import User
import traceback
from opskit_api.common.login_helper import auth_decorator


class AdminUser(Resource):

    method_decorators = [auth_decorator]

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):

        try:
            self.parser.add_argument(
                'page', type=int, required=False, location='args', default=1)
            self.parser.add_argument(
                'pagesize', type=int, required=False, location='args', default=10)
            self.parser.add_argument(
                'username', type=str, required=False, location='args', default=None)
            self.parser.add_argument(
                'is_auditing', type=int, required=False, location='args', default=None)
            args = self.parser.parse_args()
            username = g.username
            is_auditing = True if args.is_auditing else False
            user_ins = User.query.filter_by(user_name=username).first()
            if user_ins and user_ins.user_role.code == 1:
                if args.username and not is_auditing:
                    user_total = User.query.filter(User.user_name.contains(args.username)).order_by(
                        User.create_time.desc()).count()
                    user_ins_list = User.query.filter(User.user_name.contains(args.username)).order_by(
                        User.create_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                elif is_auditing and not args.username:
                    user_total = User.query.filter(User.is_auditing == is_auditing).order_by(
                        User.create_time.desc()).count()
                    user_ins_list = User.query.filter(User.is_auditing == is_auditing).order_by(
                        User.create_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                elif is_auditing and args.username:
                    user_total = User.query.filter(User.user_name.contains(args.username), User.is_auditing == is_auditing).order_by(
                        User.create_time.desc()).count()
                    user_ins_list = User.query.filter(User.user_name.contains(args.username), User.is_auditing == is_auditing).order_by(
                        User.create_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                else:
                    user_total = User.query.order_by(User.create_time.desc()).count()
                    user_ins_list = User.query.order_by(User.create_time.desc()).limit(
                        args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                user_info_list = [
                    {
                        "username": item.user_name,
                        "email": item.user_email,
                        "role": item.user_role.value,
                        "avatar": item.user_avatar,
                        "create_time": item.create_time,
                        "is_auditing": item.is_auditing,
                        "essay_count": item.note_set.count()
                    } for item in user_ins_list

                ]
            else:
                return {'code': 1, 'msg': "无操作权限"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取用户信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': user_info_list, 'total': user_total}

    def put(self):

        self.parser.add_argument(
            'username', type=str, required=True, location='json')
        self.parser.add_argument(
            'is_auditing', type=bool, required=True, location='json')
        args = self.parser.parse_args()
        try:
            username = g.username
            current_app.logger.info(args)
            admin_user = User.query.filter_by(user_name=username).first()
            if admin_user and admin_user.user_role.code == 1:
                user_ins = User.query.filter_by(
                    user_name=args.username).first()
                if user_ins:
                    user_ins.is_auditing = args.is_auditing
                    user_ins.update()
                else:
                    return {'code': 1, 'msg': "用户不存在"}
            else:
                return {'code': 1, 'msg': "无权限操作"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '更新用户信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功"}
