from flask_restful import Resource
from flask_restful import reqparse
from flask import g, current_app
from opskit_api.models import Message, User
import traceback
from opskit_api.common.login_helper import auth_decorator


class UserMessage(Resource):

    method_decorators = [auth_decorator]

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self):
        self.parser.add_argument(
            "state", type=str, required=False, default="all", location="args"
        )
        args = self.parser.parse_args()
        try:
            msg_list = []
            user = User.query.filter_by(user_name=g.username).first()
            if args.state not in ["0", "1"]:
                return {"code": 3, "msg": "不存在的消息状态"}

            if args.state == "all":
                msgs = Message.query.filter_by(user=user).all()
            else:
                msgs = Message.query.filter_by(user=user, state=int(args.state)).all()

            for item in msgs:
                msg_list.append(
                    {
                        "id": item.id,
                        "state": item.state,
                        "msg_type": item.msg_type,
                        "content": item.content,
                        "msg_link": item.msg_link,
                        "createtime": item.create_time,
                    }
                )
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {"code": 1, "msg": "获取消息异常"}
        else:
            return {"code": 0, "msg": "请求成功", "data": msg_list}

    def put(self):

        self.parser.add_argument("id", type=str, required=True, location="json")
        args = self.parser.parse_args()
        try:
            user = User.query.filter_by(user_name=g.username).first()
            msgs = Message.query.filter_by(user=user, id=args.id).first()
            msgs.state = 1
            msgs.save()
        except Exception:
            current_app.logger.error(traceback.format_exc())
            return {"code": 1, "msg": "处理消息异常"}
        else:
            return {"code": 0, "msg": "请求成功"}
