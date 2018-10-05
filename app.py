from flask import Blueprint
from flask_restful import Api

# 引入视图函数
from opskit_api.resources.api.helloworld import HelloWorld
from opskit_api.resources.auth.login import Login
from opskit_api.resources.auth.register import Register
from opskit_api.models import app, User, Note, db, migrate

#api blueprint
api_bp = Blueprint('api', __name__)

api_resource = Api(api_bp, catch_all_404s=True)

api_resource.add_resource(HelloWorld, '/')



#auth blueprint
auth_bp = Blueprint('auth', __name__)

auth_resource = Api(auth_bp, catch_all_404s=True)

auth_resource.add_resource(Login, '/login')
auth_resource.add_resource(Register, '/register')

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')
