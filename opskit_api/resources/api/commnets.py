from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app, g
from opskit_api.models import Comment, User, Note
from opskit_api.common.login_helper import common_decorator
import traceback
from datetime import datetime


class Comments(Resource):

    method_decorators = {
        'post': [common_decorator]
    }

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument('page', type=int, default=1, location='args')
        self.parser.add_argument(
            'page_size', type=int, default=10, location='args')
        self.parser.add_argument('note_id', type=str, required=True, location='args')
        args = self.parser.parse_args()
        try:
            note = Note.query.filter_by(id=args.note_id).first()
            if not note:
                return {'code': 2, 'msg': '文章不存在'}
            comment_list = Comment.query.filter(Comment.state == 1, Comment.note == note).order_by(
                Comment.create_time.desc()).limit(args.page_size).offset(args.page_size * (args.page - 1)).all()
            comment_total = Comment.query.filter(Comment.state == 1, Comment.note == note).count()
            comment_infos = [
                {
                    'id': item.id,
                    'content': item.content,
                    'prase_count': item.prase_count,
                    'username': item.user.user_name,
                    'create_time': item.create_time,
                    'update_time': item.update_time,
                    'useravatar': item.user.user_avatar
                } for item in comment_list
            ]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': '请求失败'}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': comment_infos, 'total': comment_total}

    def post(self):
        self.parser.add_argument(
            'id', type=str, required=True, location='json')
        self.parser.add_argument(
            'content', type=str, required=True, location='json')
        args = self.parser.parse_args()
        try:
            if g.username:
                user = User.query.filter_by(user_name=g.username).first()
                if not user:
                    return {'code': 2, 'msg': '用户不存在'}
                note = Note.query.filter_by(id=args.id).first()
                if not note:
                    return {'code': 2, 'msg': '文章不存在'}
                if user.user_role.code == 1:
                    Comment(user=user, 
                            note=note, 
                            update_time=datetime.utcnow(),
                            create_time=datetime.utcnow(),
                            state = 1,
                            content=args.content
                    ).save()
                else:
                    Comment(user=user, 
                            note=note, 
                            update_time=datetime.utcnow(),
                            create_time=datetime.utcnow(),
                            content=args.content
                    ).save()

            else:
                return {'code': 2, 'msg': '评论前请登录'}
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "评论成功"}
