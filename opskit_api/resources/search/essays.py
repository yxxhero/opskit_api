from flask_restful import Resource, reqparse
from flask import current_app
from opskit_api.models import Note
from sqlalchemy import or_
import traceback


class SearchNote(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):

        try:
            self.parser.add_argument(
                "page", type=int, required=False, location="args", default=1
            )
            self.parser.add_argument(
                "pagesize", type=int, required=False, location="args", default=10
            )
            self.parser.add_argument(
                "keyword", type=str, required=False, location="args", default=None
            )
            args = self.parser.parse_args()
            if args.keyword:
                note_total = (
                    Note.query.filter(
                        or_(
                            Note.content.contains(args.keyword),
                            Note.title.contains(args.keyword),
                        ),
                        Note.is_public == True,
                    )
                    .order_by(Note.update_time.desc())
                    .count()
                )
                note_ins_list = (
                    Note.query.filter(
                        or_(
                            Note.content.contains(args.keyword),
                            Note.title.contains(args.keyword),
                        ),
                        Note.is_public == True,
                    )
                    .order_by(Note.update_time.desc())
                    .limit(args.pagesize)
                    .offset(args.pagesize * (args.page - 1))
                    .all()
                )
            else:
                note_total = (
                    Note.query.filter(Note.is_public == True)
                    .order_by(Note.update_time.desc())
                    .count()
                )
                note_ins_list = (
                    Note.query.filter(Note.is_public == True)
                    .order_by(Note.update_time.desc())
                    .limit(args.pagesize)
                    .offset(args.pagesize * (args.page - 1))
                    .all()
                )

            note_info_list = [
                {
                    "username": item.user.user_name,
                    "id": item.id,
                    "view_count": item.view_count,
                    "comment_count": item.note_comments.count(),
                    "title": item.title,
                    "avatar": item.user.user_avatar,
                    "create_time": item.create_time,
                    "update_time": item.update_time,
                    "is_public": item.is_public,
                    "note_type": item.note_type.value,
                }
                for item in note_ins_list
            ]
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {"code": 1, "msg": "获取文章信息异常"}
        else:
            return {
                "code": 0,
                "msg": "请求成功",
                "data": note_info_list,
                "total": note_total,
            }
