from flask_restful import Resource, reqparse
from flask import g, current_app
from opskit_api.models import Comment, User
import traceback
from opskit_api.common.login_helper import auth_decorator


class AdminComment(Resource):

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
                'state', type=str, required=False, location='args', default=0)
            args = self.parser.parse_args()
            username = g.username
            user_ins = User.query.filter_by(user_name=username).first()
            if user_ins and user_ins.user_role.code == 1:
                comment_total = Comment.query.filter(Comment.state == args.state).order_by(Comment.update_time.desc()).count()
                comment_ins_list = Comment.query.filter(Comment.state == args.state).order_by(Comment.update_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                comment_info_list = [
                    {
                        "username": item.user.user_name,
                        "id": item.id,
                        "content": item.content,
                        "prase_count": item.prase_count,
                        "title": item.note.title,
                        "avatar": item.user.user_avatar,
                        "create_time": item.create_time,
                        "update_time": item.update_time,
                        "state": item.state,
                        "note_type": item.note.note_type.value
                    } for item in comment_ins_list

                ]
            else:
                return {'code': 1, 'msg': "无操作权限"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取文章信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': comment_info_list, 'total': comment_total}

    def put(self):

        self.parser.add_argument(
            'id', type=str, required=True, location='json')
        self.parser.add_argument(
            'state', type=int, required=True, location='json')
        args = self.parser.parse_args()
        try:
            username = g.username
            admin_user = User.query.filter_by(user_name=username).first()
            if admin_user and admin_user.user_role.code == 1:
                comment_ins = Comment.query.filter_by(
                    id=args.id).first()
                if comment_ins:
                    comment_ins.state = args.state
                    comment_ins.update()
                else:
                    return {'code': 1, 'msg': "评论不存在"}
            else:
                return {'code': 1, 'msg': "无权限操作"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '更新评论信息异常'}
        else:
            return {'code': 0, 'msg': "更新成功"}

    def delete(self):

        self.parser.add_argument(
            'id', type=str, required=True, location='json')
        args = self.parser.parse_args()
        try:
            username = g.username
            admin_user = User.query.filter_by(user_name=username).first()
            if admin_user and admin_user.user_role.code == 1:
                comment_ins = Comment.query.filter_by(
                    id=args.id).first()
                if comment_ins:
                    comment_ins.remove()
                else:
                    return {'code': 1, 'msg': "评论不存在"}
            else:
                return {'code': 1, 'msg': "无权限操作"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '更新评论信息异常'}
        else:
            return {'code': 0, 'msg': "更新成功"}
