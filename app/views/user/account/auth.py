from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token
from schematics.types import EmailType, StringType
from werkzeug.security import check_password_hash

from app.context import context_property
from app.decorators.validation import PayloadLocation, BaseModel, validate_with_schematics
from app.extensions import main_db
from app.models.user import TblUsers
from app.views.base import BaseResource


class AuthAPI(BaseResource):
    class Schema:
        class Post(BaseModel):
            id = StringType(
                serialized_name='id',
                required=True
            )

            password = StringType(
                serialized_name='password',
                required=True,
                min_length=8
            )

    @validate_with_schematics(PayloadLocation.JSON, Schema.Post)
    def post(self):
        """
        로그인 API
        """

        payload: self.Schema.Post = context_property.request_payload_object
        session = main_db.session

        user: TblUsers = TblUsers.get_first_without_none_check(
            session,
            TblUsers.id == payload.id
        )

        if user is None or not check_password_hash(user.password, payload.password):
            abort(401)
        else:
            return {
                'accessToken': create_access_token(user.id),
                'refreshToken': create_refresh_token(user.id)
            }, 201
