from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app
from opskit_api.models import Note
import traceback

NOTE_TYPES = {
    "database": 1,
    "web": 2,
    "docker": 3,
    "security": 4,
    "notice": 5,
    "hadoop": 6,
    "opsai": 7,
    "opsbase": 8,
    "opsskill": 9,
    "opsframework": 10,
}


class Essays(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument("page", type=int, default=1, location="args")
        self.parser.add_argument("page_size", type=int, default=10, location="args")
        self.parser.add_argument("note_type", type=str, default=None, location="args")
        args = self.parser.parse_args()
        try:
            if args.note_type:
                if args.note_type in NOTE_TYPES.keys():
                    note_list = (
                        Note.query.filter(
                            Note.is_public == True,
                            Note.note_type == NOTE_TYPES[args.note_type],
                        )
                        .order_by(Note.create_time.desc())
                        .limit(args.page_size)
                        .offset(args.page_size * (args.page - 1))
                        .all()
                    )
                    note_total = Note.query.filter(
                        Note.is_public == True,
                        Note.note_type == NOTE_TYPES[args.note_type],
                    ).count()
                else:
                    return {"code": 1, "msg": "类目不存在"}
            else:
                note_list = (
                    Note.query.filter(Note.is_public == True)
                    .order_by(Note.create_time.desc())
                    .limit(args.page_size)
                    .offset(args.page_size * (args.page - 1))
                    .all()
                )
                note_total = Note.query.filter(Note.is_public == True).count()
            note_infos = [
                {
                    "view_count": item.view_count,
                    "href": "/essay/view/?note_id=" + str(item.id),
                    "content": item.content,
                    "note_type": item.note_type.value,
                    "raw_content": item.raw_content,
                    "title": item.title,
                    "comment_count": item.note_comments.count(),
                    "username": item.user.user_name,
                    "useravatar": item.user.user_avatar,
                }
                for item in note_list
            ]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {"code": 1, "msg": str(e)}
        else:
            return {"code": 0, "msg": "请求成功", "data": note_infos, "total": note_total}
