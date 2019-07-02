import os
import traceback
import time
from datetime import datetime
from flask import g, current_app
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from opskit_api.common.login_helper import auth_decorator
from opskit_api.common.upload_helper import allowed_file, ensure_userdir_exist
from opskit_api.common.paasswordmd5 import md5passwd
from opskit_api.models import Uploads, User


class Upload(Resource):

    method_decorators = {"post": [auth_decorator]}

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.parser.add_argument(
            "file", type=FileStorage, location="files", required=True
        )
        self.parser.add_argument("is_avatar", type=str, location="form", required=False)
        args = self.parser.parse_args()
        if not allowed_file(args.file.filename):
            return {"code": 1, "msg": "文件名不合法"}
        try:
            filename = secure_filename(args.file.filename)
            md5_value = md5passwd(filename + str(time.time()))
            md5_filename = md5_value + "." + filename.split(".")[1]
            file_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], username)
            username = g.username
            if args.is_avatar == "1":
                ensure_userdir_exist(file_dir)
                args.file.save(os.path.join(file_dir, md5_filename))
                user = User.query.filter_by(user_name=username).first()
                Uploads(
                    user=user,
                    image_path=os.path.join(file_dir, md5_filename),
                    create_time=datetime.now(),
                ).save()
                user.user_avatar = current_app.config["IMAGE_HOST"] + os.path.join(
                    "/uploads/", username, md5_filename
                )
                user.update()
            else:
                if not (user.user_role.code == 1 or user.is_auditing):
                    return {"code": 2, "msg": "无权上传图片"}
                user = User.query.filter_by(user_name=username).first()
                file_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], username)
                ensure_userdir_exist(file_dir)
                args.file.save(os.path.join(file_dir, md5_filename))
                Uploads(
                    user=user,
                    image_path=os.path.join(file_dir, md5_filename),
                    create_time=datetime.now(),
                ).save()
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {"code": 3, "msg": str(e)}
        else:
            return {
                "code": 0,
                "url": current_app.config["IMAGE_HOST"]
                + os.path.join("/uploads/", username, md5_filename),
                "msg": "上传文件成功",
            }
