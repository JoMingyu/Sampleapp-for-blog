from flask import abort
from flask_jwt_extended import jwt_required
from schematics.types import StringType
from sqlalchemy.exc import IntegrityError

from app.context import context_property
from app.decorators.validation import PayloadLocation, BaseModel, validate_with_schematics
from app.extensions import main_db
from app.models.comment import TblComments
from app.views.base import BaseResource


class CommentAPI(BaseResource):
    class Schema:
        class Post(BaseModel):
            content = StringType(
                serialized_name='content',
                required=True,
                max_length=TblComments.content.type.length
            )

    @validate_with_schematics(PayloadLocation.JSON, Schema.Post)
    @jwt_required
    def post(self, post_id):
        """
        댓글 작성 API
        """

        payload: self.Schema.Post = context_property.request_payload_object
        session = main_db.session
        user = context_property.requested_user

        try:
            comment = TblComments(
                content=payload.content,
                owner_id=user.id,
                post_id=post_id
            )

            session.add(comment)
            session.commit()
            session.refresh(comment)

            return {
                'id': comment.id
            }
        except IntegrityError:
            abort(404, 'Post ID `{}` not found.'.format(payload.category_id))

    @jwt_required
    def get(self, post_id):
        """
        댓글 목록 API
        """

        session = main_db.session

        return {
            'data': [
                comment.json for comment in TblComments.get_all(session, TblComments.post_id == post_id)
            ]
        }
