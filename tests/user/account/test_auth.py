from tests.user.account import JWTRelatedTest


class TestAuthAPI(JWTRelatedTest):
    def setUp(self):
        super(TestAuthAPI, self).setUp()

        self.method = 'POST'
        self.path = '/user/account/auth'

    def test_happypath(self):
        self.json = {
            'id': self.test_user_model.id,
            'password': self.test_user_model.password
        }

        resp = self.request()
        self.assertEqual(201, resp.status_code)

        payload = resp.json
        self.validate_jwt_token(
            payload['accessToken'],
            payload['refreshToken']
        )

    def test_invalid_id(self):
        """
        ID가 틀린 경우
        """
        self.json = {
            'id': self.test_user_model.id + '!',
            'password': self.test_user_model.password
        }

        resp = self.request()
        self.assertEqual(401, resp.status_code)

    def test_invalid_password(self):
        """
        비밀번호가 틀린 경우
        """
        self.json = {
            'id': self.test_user_model.id,
            'password': self.test_user_model.password + '!'
        }

        resp = self.request()
        self.assertEqual(401, resp.status_code)
