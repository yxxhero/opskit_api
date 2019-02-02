import os
from opskit_api.models import app


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def ensure_userdir_exist(userdir):
    os.makedirs(userdir, exist_ok=True)
