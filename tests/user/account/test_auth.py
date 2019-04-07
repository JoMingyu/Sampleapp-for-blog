from werkzeug.security import generate_password_hash

from app.models.user import TblUsers
from app.views.user.account.signup import SignupAPI

from tests.user.account import JWTRelatedTestBase


class TestAuthAPI(JWTRelatedTestBase):
    def setUp(self):
        super(TestAuthAPI, self).setUp()

        self.method = 'POST'
        self.path = '/user/account/auth'

        self.mock_object = SignupAPI.Schema.Post.get_mock_object()
        with self.app.test_request_context():
            self.session.add(TblUsers(
                id=self.mock_object.id,
                password=generate_password_hash(self.mock_object.password),
                nickname=self.mock_object.nickname
            ))
            self.session.commit()

    def test_happypath(self):
        self.json = {
            'id': self.mock_object.id,
            'password': self.mock_object.password
        }

        resp = self.request()
        self.assertEqual(201, resp.status_code)

        payload = resp.json
        self.validate_jwt_token(
            payload['accessToken'],
            payload['refreshToken'],
            self.app.secret_key,
            self.json['id']
        )

    def test_invalid_id(self):
        """
        ID가 틀린 경우
        """
        self.json = {
            'id': self.mock_object.id + '!',
            'password': self.mock_object.password
        }

        resp = self.request()
        self.assertEqual(401, resp.status_code)

    def test_invalid_password(self):
        """
        비밀번호가 틀린 경우
        """
        self.json = {
            'id': self.mock_object.id,
            'password': self.mock_object.password + '!'
        }

        resp = self.request()
        self.assertEqual(401, resp.status_code)
