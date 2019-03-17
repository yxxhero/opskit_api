from flask_restful import Resource, reqparse
from flask import g, current_app
from opskit_api.models import Note, User, Comment
import traceback
from opskit_api.common.login_helper import auth_decorator


class AdminNote(Resource):

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
                'keyword', type=str, required=False, location='args', default=None)
            self.parser.add_argument(
                'is_public', type=int, required=False, location='args', default=None)
            args = self.parser.parse_args()
            username = g.username
            is_public = True if args.is_public == 1 else False
            user_ins = User.query.filter_by(user_name=username).first()
            if user_ins and user_ins.user_role.code == 1:
                if args.keyword and args.is_public == None:
                    note_total = Note.query.filter(Note.content.contains(args.keyword)).order_by(
                        Note.update_time.desc()).count()
                    note_ins_list = Note.query.filter(Note.content.contains(args.keyword)).order_by(
                        Note.update_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                elif args.is_public != None and not args.keyword:
                    note_total = Note.query.filter(Note.is_public == is_public).order_by(
                        Note.update_time.desc()).count()
                    note_ins_list = Note.query.filter(Note.is_public == is_public).order_by(
                        Note.update_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                elif args.is_public != None and args.keyword:
                    note_total = Note.query.filter(Note.content.contains(args.keyword), Note.is_public == is_public).order_by(Note.update_time.desc()).count()
                    note_ins_list = Note.query.filter(Note.content.contains(args.keyword), Note.is_public == is_public).order_by(Note.update_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                else:
                    note_total = Note.query.order_by(Note.update_time.desc()).count()
                    note_ins_list = Note.query.order_by(Note.update_time.desc()).limit(args.pagesize).offset(args.pagesize * (args.page - 1)).all()
                note_info_list = [
                    {
                        "username": item.user.user_name,
                        "id": item.id,
                        "view_count": item.view_count,
                        "title": item.title,
                        "avatar": item.user.user_avatar,
                        "create_time": item.create_time,
                        "update_time": item.update_time,
                        "is_public": item.is_public,
                        "note_type": item.note_type.value
                    } for item in note_ins_list

                ]
            else:
                return {'code': 1, 'msg': "无操作权限"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '获取文章信息异常'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': note_info_list, 'total': note_total}

    def put(self):

        self.parser.add_argument(
            'id', type=str, required=True, location='json')
        self.parser.add_argument(
            'is_public', type=bool, required=True, location='json')
        args = self.parser.parse_args()
        current_app.logger.error(args)

        try:
            username = g.username
            admin_user = User.query.filter_by(user_name=username).first()
            if admin_user and admin_user.user_role.code == 1:
                note_ins = Note.query.filter_by(
                    id=args.id).first()
                if note_ins:
                    note_ins.is_public = args.is_public
                    note_ins.update()
                else:
                    return {'code': 1, 'msg': "文章不存在"}
            else:
                return {'code': 1, 'msg': "无权限操作"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '更新文章信息异常'}
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
                note_ins = Note.query.filter_by(
                    id=args.id).first()
                if note_ins:
                    comment_list = Comment.query.filter_by(note=note_ins).all()
                    
                    for item in comment_list:
                        item.remove()
                    note_ins.remove()
                else:
                    return {'code': 1, 'msg': "文章不存在"}
            else:
                return {'code': 1, 'msg': "无权限操作"}
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '删除文章异常'}
        else:
            return {'code': 0, 'msg': "删除成功"}
