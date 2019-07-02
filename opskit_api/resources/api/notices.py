from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app
from opskit_api.models import Note
import traceback


class Notices(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        try:
            note_list = (
                Note.query.filter(Note.is_public == True, Note.note_type == 5)
                .order_by(Note.create_time.desc())
                .limit(2)
                .all()
            )
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
            return {"code": 0, "msg": "请求成功", "data": note_infos}
