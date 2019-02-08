from flask_restful import Resource
from flask import current_app
from opskit_api.models import Note
import traceback


class Recommend(Resource):

    def get(self):
        try:
            note_list = Note.query.order_by(Note.view_count.desc()).limit(10)
            recommend_list = [{
                "href": "/essay/view/?note_id=" + str(note_ins.id),
                "id": note_ins.id, 
                "title": note_ins.title,
                "content": note_ins.content,
                "raw_content": note_ins.raw_content,
                "view_count": note_ins.view_count,
                "username": note_ins.user.user_name,
                "useravatar": note_ins.user.user_avatar,
                "createtime": note_ins.create_time,
                "updatetime": note_ins.update_time
            } for note_ins in note_list]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "请求成功", 'data': recommend_list}
