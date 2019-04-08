from app.models.category import TblCategories
from app.views.board.category import CategoryAPI
from tests import BaseTest


class TestCategoryPostAPI(BaseTest):
    def setUp(self):
        super(TestCategoryPostAPI, self).setUp()

        self.method = 'POST'
        self.uri = '/board/categories'
        self.set_authorization_header_jwt(self.test_user_access_token)

    def test_happypath(self):
        self.json = CategoryAPI.Schema.Post.get_mock_object().to_primitive()
        resp = self.request()
        self.assertEqual(201, resp.status_code)

        payload = resp.json
        self.assertDictEqual({
            'id': 1
        }, payload)

    def test_category_name_duplicated(self):
        name = self.generate_random_string()

        self.session.add(
            TblCategories(
                name=name
            )
        )
        self.session.commit()

        self.json = {
            'name': name
        }
        resp = self.request()
        self.assertEqual(409, resp.status_code)


class TestCategoryGetAPI(BaseTest):
    def setUp(self):
        super(TestCategoryGetAPI, self).setUp()

        self.uri = '/board/categories'
        self.set_authorization_header_jwt(self.test_user_access_token)

    def test_happypath(self):
        category_names = [
            self.generate_random_string() for _ in range(10)
        ]

        for category_name in category_names:
            self.session.add(
                TblCategories(
                    name=category_name
                )
            )
        self.session.commit()

        resp = self.request()
        self.assertEqual(200, resp.status_code)

        payload = resp.json
        self.assertDictEqual({
            'data': [{
                'id': id,
                'name': category_name
            } for id, category_name in zip(range(1, 11), category_names)]
        }, payload)

    def test_empty_category_list(self):
        resp = self.request()
        self.assertEqual(200, resp.status_code)

        payload = resp.json
        self.assertDictEqual({
            'data': []
        }, payload)
