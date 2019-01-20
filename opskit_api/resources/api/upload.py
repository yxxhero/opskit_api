import os
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from opskit_api.common.login_helper import auth_decorator, jwt_decode_token
from opskit_api.common.upload_helper import allowed_file, ensure_userdir_exist
from opskit_api.models import app


class Upload(Resource):

    method_decorators = {'post': [auth_decorator]}

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.parser.add_argument(
            'file', type=FileStorage, location='files', required=True)
        args = self.parser.parse_args()
        if not allowed_file(args.file.filename):
            return {'code': 403, 'msg': "文件名不合法"}
        try:
            filename = secure_filename(args.file.filename)
            username = jwt_decode_token(request.headers.get('Authorization'))[
                'data']['username']
            file_dir = os.path.join(app.config['UPLOAD_FOLDER'], username)
            ensure_userdir_exist(file_dir)
            args.file.save(os.path.join(file_dir, filename))
        except Exception as e:
            return {'code': 1, 'msg': str(e)}
        else:
            return {'code': 0, 'msg': "上传文件成功"}
