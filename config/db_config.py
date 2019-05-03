import os


DB_NAME = 'stay'


class LocalDBConfig:
    MAIN_DB_URL = 'mysql+mysqldb://root:toor@localhost:3306/{}?charset=utf8mb4'.format(
        DB_NAME
    )


class RemoteDBConfig:
    MAIN_DB_URL = 'mysql+mysqldb://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_ENDPOINT'),
        DB_NAME
    )
