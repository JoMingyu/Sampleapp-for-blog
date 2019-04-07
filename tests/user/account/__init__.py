from jwt import decode

from werkzeug.security import generate_password_hash

from app.models.user import TblUsers
from app.views.user.account.signup import SignupAPI
from tests import BaseTest


class JWTRelatedTestBase(BaseTest):
    def setUp(self):
        super(JWTRelatedTestBase, self).setUp()

        self.mock_object = SignupAPI.Schema.Post.get_mock_object()
        with self.app.test_request_context():
            self.session.add(TblUsers(
                id=self.mock_object.id,
                password=generate_password_hash(self.mock_object.password),
                nickname=self.mock_object.nickname
            ))
            self.session.commit()

    def _validate_access_token(self, access_token, secret_key, expected_identity):
        access_token_payload: dict = decode(access_token, secret_key)
        self.assertEqual('access', access_token_payload['type'])
        self.assertEqual(expected_identity, access_token_payload['identity'])

    def _validate_refresh_token(self, refresh_token, secret_key, expected_identity):
        refresh_token_payload: dict = decode(refresh_token, secret_key)
        self.assertEqual('refresh', refresh_token_payload['type'])
        self.assertEqual(expected_identity, refresh_token_payload['identity'])

    def validate_jwt_token(self, access_token: str, refresh_token: str, secret_key: str, expected_identity: str):
        self._validate_access_token(access_token, secret_key, expected_identity)
        self._validate_refresh_token(refresh_token, secret_key, expected_identity)
