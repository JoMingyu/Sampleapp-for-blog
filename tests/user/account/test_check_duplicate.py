from app.models.user import TblUsers

from tests import BaseTest


class TestIDDuplicateCheckAPI(BaseTest):
    def setUp(self):
        super(TestIDDuplicateCheckAPI, self).setUp()
        
        self.path = '/user/account/check-duplicate/id/{id}'

    def test_happypath(self):
        self.path_parameters = {
            'id': self.generate_random_string()
        }

        resp = self.request()

        self.assertEqual(200, resp.status_code)

    def test_id_duplicate(self):
        id_will_be_duplicate = self.generate_random_string()

        self.session.add(TblUsers(
            id=id_will_be_duplicate,
            password=self.generate_random_string(),
            nickname=self.generate_random_string()
        ))

        self.session.commit()

        self.path_parameters = {
            'id': id_will_be_duplicate
        }

        resp = self.request()

        self.assertEqual(409, resp.status_code)
