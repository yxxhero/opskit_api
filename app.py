from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
import logging

# 引入视图函数
from opskit_api.resources.api.essays import Essays
from opskit_api.resources.api.useressays import UserEssays
from opskit_api.resources.api.essay import Essay
from opskit_api.resources.api.upload import Upload
from opskit_api.resources.api.userinfo import UserInfo
from opskit_api.resources.admin.users import AdminUser
from opskit_api.resources.admin.essays import AdminNote
from opskit_api.resources.admin.comments import AdminComment
from opskit_api.resources.api.commnets import Comments
from opskit_api.resources.search.essays import SearchNote
from opskit_api.resources.auth.login import Login
from opskit_api.resources.auth.logout import Logout
from opskit_api.resources.auth.register import Register
from opskit_api.resources.statistics.recommend import Recommend
from opskit_api.models import app

CORS(app, resources={r"/api/*": {"origins": "*"}})

# resources blueprint
api_bp = Blueprint('api', __name__)

api_resource = Api(api_bp, catch_all_404s=True)

api_resource.add_resource(Essays, '/notes')
api_resource.add_resource(UserEssays, '/usernotes')
api_resource.add_resource(Essay, '/note')
api_resource.add_resource(Upload, '/upload')
api_resource.add_resource(UserInfo, '/userinfo')
api_resource.add_resource(Comments, '/comments')

# admin blueprint
admin_bp = Blueprint('admin', __name__)

admin_resource = Api(admin_bp, catch_all_404s=True)

admin_resource.add_resource(AdminUser, '/users')
admin_resource.add_resource(AdminNote, '/notes')
admin_resource.add_resource(AdminComment, '/comments')

# auth blueprint
auth_bp = Blueprint('auth', __name__)

auth_resource = Api(auth_bp, catch_all_404s=True)

auth_resource.add_resource(Login, '/login')
auth_resource.add_resource(Logout, '/logout')
auth_resource.add_resource(Register, '/register')

# statistics blueprint

statistics_bp = Blueprint('statistics', __name__)

statistics_resource = Api(statistics_bp, catch_all_404s=True)

statistics_resource.add_resource(Recommend, '/recommend')


# search blueprint

search_bp = Blueprint('search', __name__)

search_resource = Api(search_bp, catch_all_404s=True)

search_resource.add_resource(SearchNote, '/notes')


# 拦截请求
@app.before_request
def handle_token():
    pass


# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(search_bp, url_prefix='/api/v1/search')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
app.register_blueprint(api_bp, url_prefix='/api/v1/resource')
app.register_blueprint(statistics_bp, url_prefix='/api/v1/statistics')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
