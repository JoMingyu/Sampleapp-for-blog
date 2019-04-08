from jwt import decode

from tests import BaseTest


class JWTRelatedTest(BaseTest):
    def _validate_access_token(self, access_token, secret_key, expected_identity):
        access_token_payload: dict = decode(access_token, secret_key)
        self.assertEqual('access', access_token_payload['type'])
        self.assertEqual(expected_identity, access_token_payload['identity'])

    def _validate_refresh_token(self, refresh_token, secret_key, expected_identity):
        refresh_token_payload: dict = decode(refresh_token, secret_key)
        self.assertEqual('refresh', refresh_token_payload['type'])
        self.assertEqual(expected_identity, refresh_token_payload['identity'])

    def validate_jwt_token(self, access_token: str, refresh_token: str, secret_key=None, expected_identity=None):
        secret_key = secret_key or self.app.secret_key
        expected_identity = expected_identity or self.test_user_model.id

        self._validate_access_token(access_token, secret_key, expected_identity)
        self._validate_refresh_token(refresh_token, secret_key, expected_identity)
