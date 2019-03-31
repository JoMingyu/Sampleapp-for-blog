import random
from string import printable
from unittest import TestCase

from flask.wrappers import ResponseBase

from app import create_app
from app.extensions import main_db
from app.models import Base
from config import app_config, db_config


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(
            app_config.LocalLevelConfig,
            db_config.LocalDBConfig
        )

        cls.client = cls.app.test_client()
        cls.session = main_db.checkout_new_session()

        cls.method = 'GET'
        cls.path = None
        cls.path_parameters = dict()

        cls.json = dict()
        cls.query_string = dict()

    def setUp(self):
        Base.metadata.create_all(main_db.engine)

    def tearDown(self):
        Base.metadata.drop_all(main_db.engine)

    def request(self) -> ResponseBase:
        return self.client.open(
            method=self.method,
            path=self.path.format(**self.path_parameters),
            json=self.json,
            query_string=self.query_string
        )

    def generate_random_string(self, length=10):
        return ''.join(random.choice(printable) for _ in range(length))
