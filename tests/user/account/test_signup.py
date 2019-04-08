from app.views.user.account.signup import SignupAPI

from tests import BaseTest


class TestSignupAPI(BaseTest):
    def setUp(self):
        super(TestSignupAPI, self).setUp()

        self.method = 'POST'
        self.path = '/user/account/signup'

    def test_happypath(self):
        self.json = SignupAPI.Schema.Post.get_mock_object().mock_object.to_primitive()
        resp = self.request()

        self.assertEqual(201, resp.status_code)

        # self.assertEqual(1, self.session.query(TblUsers).count())
        # TODO

    def test_id_duplicate(self):
        self.json = self.test_user_model.to_primitive()

        resp = self.request()

        self.assertEqual(409, resp.status_code)
