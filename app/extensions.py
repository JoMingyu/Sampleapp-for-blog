from flask_jwt_extended import JWTManager

from app.models import MainDB


jwt = JWTManager()
main_db = MainDB()
