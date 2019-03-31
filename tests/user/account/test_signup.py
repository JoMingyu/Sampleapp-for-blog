from app.models.user import TblUsers
from app.views.user.account.signup import SignupAPI

from tests import BaseTest


class TestSignupAPI(BaseTest):
    def setUp(self):
        super(TestSignupAPI, self).setUp()

        self.method = 'POST'
        self.path = '/user/account/signup'
        self.mock_object = SignupAPI.Schema.Post.get_mock_object()
        self.json = self.mock_object.to_primitive()

    def test_happypath(self):
        resp = self.request()

        self.assertEqual(201, resp.status_code)

        # self.assertEqual(1, self.session.query(TblUsers).count())
        # TODO

    def test_id_duplicate(self):
        self.session.add(TblUsers(
            id=self.mock_object.id,
            password=self.mock_object.password,
            nickname=self.mock_object.nickname
        ))

        self.session.commit()

        resp = self.request()

        self.assertEqual(409, resp.status_code)
