from flask import Blueprint, Flask
from flask_restful import Api


def route(flask_app: Flask):
    from app.views.user.account import auth, check_duplicate, refresh, signup, verify

    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception
    # register_blueprint 시 defer되었던 함수들이 호출되며, flask-restful.Api._init_app()이 호출되는데
    # 해당 메소드가 app 객체의 에러 핸들러를 오버라이딩해서, 별도로 적용한 handler의 HTTPException 관련 로직이 동작하지 않음
    # 따라서 두 함수를 임시 저장해 두고, register_blueprint 이후 함수를 재할당하도록 함

    # - blueprint, api object initialize
    api_v1_blueprint = Blueprint('api_v1', __name__)
    api_user__account = Api(api_v1_blueprint, prefix='/user/account')

    # - route
    api_user__account.add_resource(check_duplicate.IDDuplicateCheckAPI, '/check-duplicate/id/<id>')
    api_user__account.add_resource(signup.SignupAPI, '/signup')
    api_user__account.add_resource(auth.AuthAPI, '/auth')
    api_user__account.add_resource(refresh.RefreshAPI, '/refresh')

    # - register blueprint
    flask_app.register_blueprint(api_v1_blueprint)

    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func
