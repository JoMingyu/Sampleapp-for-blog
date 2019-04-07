from jwt import decode

from tests import BaseTest


class JWTRelatedTestBase(BaseTest):
    def validate_jwt_token(self, access_token, refresh_token, secret_key, expected_identity):
        access_token_payload: dict = decode(access_token, secret_key)
        refresh_token_payload: dict = decode(refresh_token, secret_key)

        self.assertEqual('access', access_token_payload['type'])
        self.assertEqual('refresh', refresh_token_payload['type'])
        self.assertEqual(expected_identity, access_token_payload['identity'])
        self.assertEqual(expected_identity, refresh_token_payload['identity'])
