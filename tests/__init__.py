import random
from string import printable
from unittest import TestCase

from flask.wrappers import ResponseBase
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import main_db
from app.models import Base
from app.models.user import TblUsers
from app.views.user.account.signup import SignupAPI
from config import app_config, db_config


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(
            app_config.LocalLevelConfig,
            db_config.LocalDBConfig
        )
        cls.client = cls.app.test_client()

        cls.session = main_db.checkout_new_session()

        cls.method = 'GET'
        cls.path = None
        cls.path_parameters = dict()

        cls.headers = dict()
        cls.json = dict()
        cls.query_string = dict()

    def setUp(self):
        Base.metadata.create_all(main_db.engine)

        with self.app.test_request_context():
            self.test_user_model = SignupAPI.Schema.Post.get_mock_object()
            self.test_user_access_token = create_access_token(self.test_user_model.id)

        self.session.add(TblUsers(
            id=self.test_user_model.id,
            password=generate_password_hash(self.test_user_model.password),
            nickname=self.test_user_model.nickname
        ))
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(main_db.engine)

    def escape_jwt_prefix(self, token: str):
        return token.lstrip('JWT ')

    def set_authorization_header_jwt(self, token: str):
        self.headers['Authorization'] = 'JWT {}'.format(self.escape_jwt_prefix(token))

    def request(self) -> ResponseBase:
        return self.client.open(
            method=self.method,
            path=self.path.format(**self.path_parameters),
            json=self.json,
            query_string=self.query_string
        )

    def generate_random_string(self, length=10):
        return ''.join(random.choice(printable) for _ in range(length))
