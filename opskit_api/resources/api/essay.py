from flask_restful import Resource
from flask_restful import reqparse
from flask import g, current_app
from opskit_api.models import Note, User
import traceback
from opskit_api.common.login_helper import auth_decorator, common_decorator


class Essay(Resource):

    method_decorators = {
        'post': [auth_decorator],
        'put': [auth_decorator],
        'get': [common_decorator],
        'delete': [auth_decorator]
    }

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('id', type=str, required=True, location='args')
        args = self.parser.parse_args()
        try:
            note_ins = Note.query.filter_by(id=args.id).first()
            if note_ins:
                if note_ins.is_public:
                    note_info = {
                        "title": note_ins.title,
                        "note_type": note_ins.note_type.code,
                        "content": note_ins.content,
                        "view_count": note_ins.view_count,
                        "comment_count": note_ins.note_comments.count(),
                        "raw_content": note_ins.raw_content,
                        "username": note_ins.user.user_name,
                        "useravatar": note_ins.user.user_avatar,
                        "createtime": note_ins.create_time,
                        "updatetime": note_ins.update_time
                    }
                    note_ins.view_count += 1
                    note_ins.update()
                else:
                    if g.username:
                        user = User.query.filter_by(user_name=g.username).first()
                        note_ins = Note.query.filter_by(user=user, id=args.id).first()
                        if note_ins:
                            note_info = {
                                "title": note_ins.title,
                                "note_type": note_ins.note_type.value,
                                "content": note_ins.content,
                                "view_count": note_ins.view_count,
                                "comment_count": note_ins.note_comments.count(),
                                "raw_content": note_ins.raw_content,
                                "username": note_ins.user.user_name,
                                "useravatar": note_ins.user.user_avatar,
                                "createtime": note_ins.create_time,
                                "updatetime": note_ins.update_time
                            }
                        else:
                            return {'code': 1, 'msg': "没有权限查看"}
                    else:
                        return {'code': 1, 'msg': "文章不存在或重新登录"}
            else:
                return {'code': 1, 'msg': "文章不存在"}
        except Exception:
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
            current_app.logger.info(args.raw_content)
            current_app.logger.info(args.content)
            if user.is_auditing:
                args.user = user
                Note(**args).save()
            else:
                return {'code': 1, 'msg': '账户未审核'}
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "提交成功"}

    def put(self):
        self.parser.add_argument(
            'id', type=str, required=True, location='json')
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
            note_ins = Note.query.filter_by(user=user, id=args.id).first()
            if note_ins:
                note_ins.title = args.title
                note_ins.content = args.content
                note_ins.raw_content = args.raw_content
                note_ins.note_type = args.note_type
                note_ins.update()
            else:
                return {'code': 1, 'msg': '无权限修改此文章'}

        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "提交成功"}

    def delete(self):
        self.parser.add_argument(
            'id', type=str, required=True, location='json')
        args = self.parser.parse_args()
        username = g.username
        try:
            user = User.query.filter_by(user_name=username).first()
            note_ins = Note.query.filter_by(user=user, id=args.id).first()
            if note_ins:
                note_ins.remove()
            else:
                return {'code': 1, 'msg': '无权限删除此文章'}

        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': '文章删除成功'}
