from flask import abort
from flask_jwt_extended import jwt_required
from schematics.types import StringType
from sqlalchemy.exc import IntegrityError

from app.context import context_property
from app.decorators.validation import PayloadLocation, BaseModel, validate_with_schematics
from app.extensions import main_db
from app.models.category import TblCategories
from app.views.base import BaseResource


class CategoryAPI(BaseResource):
    class Schema:
        class Post(BaseModel):
            name = StringType(
                serialized_name='name',
                required=True,
                max_length=TblCategories.name.type.length
            )

    @validate_with_schematics(PayloadLocation.JSON, Schema.Post)
    @jwt_required
    def post(self):
        """
        카테고리 추가 API
        """

        payload: self.Schema.Post = context_property.request_payload_object
        session = main_db.session
        user = context_property.requested_user

        try:
            category = TblCategories(
                name=payload.name,
                author_id=user.id
            )

            session.add(category)
            session.commit()
            session.refresh(category)

            return {
                'id': category.id
            }
        except IntegrityError:
            abort(409)

    @jwt_required
    def get(self):
        """
        카테고리 목록 조회 API
        """

        session = main_db.session

        return {
            'data': [category.json for category in TblCategories.get_all(session)]
        }
