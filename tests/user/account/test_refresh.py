from flask_jwt_extended import create_access_token, create_refresh_token

from tests.user.account import JWTRelatedTest


class TestRefreshAPI(JWTRelatedTest):
    def setUp(self):
        super(TestRefreshAPI, self).setUp()

        self.method = 'GET'
        self.path = '/user/account/refresh'

        with self.app.test_request_context():
            self.access_token = create_access_token(self.test_user_model.id)
            self.refresh_token = create_refresh_token(self.test_user_model.id)

    def test_happypath(self):
        self.set_authorization_header_jwt(self.refresh_token)

        resp = self.request()
        self.assertEqual(200, resp.status_code)

        payload = resp.json
        self._validate_access_token(
            payload['accessToken'],
            self.app.secret_key,
            self.test_user_model.id
        )

    def test_refresh_with_access_token(self):
        """
        access token을 통해 refresh
        """
        self.set_authorization_header_jwt(self.access_token)

        resp = self.request()
        self.assertEqual(401, resp.status_code)
