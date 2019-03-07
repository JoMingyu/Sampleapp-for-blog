from flask import abort
from schematics.types import EmailType, StringType
from werkzeug.security import generate_password_hash

from app.context import context_property
from app.decorators.validation import PayloadLocation, BaseModel, validate_with_schematics
from app.extensions import main_db
from app.models.user import TblUsers
from app.views.base import BaseResource


class SignupAPI(BaseResource):
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

            nickname = StringType(
                serialized_name='nickname',
                required=True,
                max_length=TblUsers.nickname.type.length
            )

    @validate_with_schematics(PayloadLocation.JSON, Schema.Post)
    def post(self):
        """
        회원가입 API
        """

        payload: self.Schema.Post = context_property.request_payload_object
        session = main_db.session

        if TblUsers.is_id_already_signed(session, payload.id):
            abort(409)
        else:
            session.add(
                TblUsers(
                    id=payload.id,
                    password=generate_password_hash(payload.password),
                    nickname=payload.nickname
                )
            )

            session.commit()

            return {}, 201
