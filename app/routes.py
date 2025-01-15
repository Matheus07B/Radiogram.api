from app.controllers.auth_controller import auth_blueprint
from app.controllers.user_controller import user_blueprint
from app.controllers.recovery_controller import recovery_blueprint

def register_routes(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(recovery_blueprint, url_prefix='/recovery')
