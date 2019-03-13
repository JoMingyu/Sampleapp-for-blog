from flask import abort
from flask_jwt_extended import jwt_required
from schematics.types import IntType, StringType
from sqlalchemy.exc import IntegrityError

from app.context import context_property
from app.decorators.validation import PayloadLocation, BaseModel, validate_with_schematics
from app.extensions import main_db
from app.models.post import TblPosts
from app.views.base import BaseResource


class PostAPI(BaseResource):
    class Schema:
        class Post(BaseModel):
            category_id = IntType(
                serialized_name='categoryID',
                required=True
            )

            title = StringType(
                serialized_name='title',
                required=True,
                max_length=TblPosts.title.type.length
            )

            content = StringType(
                serialized_name='content',
                required=True,
                max_length=TblPosts.content.type.length
            )

        class Get(BaseModel):
            category_id = IntType(
                serialized_name='category_id',
                required=True
            )

    @validate_with_schematics(PayloadLocation.JSON, Schema.Post)
    @jwt_required
    def post(self):
        """
        게시글 작성 API
        """

        payload: self.Schema.Post = context_property.request_payload_object
        session = main_db.session
        user = context_property.requested_user

        try:
            post = TblPosts(
                title=payload.title,
                content=payload.content,
                owner_id=user.id,
                category_id=payload.category_id
            )

            session.add(post)
            session.commit()
            session.refresh(post)

            return {
                'id': post.id
            }
        except IntegrityError:
            abort(404, 'category ID `{}` not found.'.format(payload.category_id))

    @validate_with_schematics(PayloadLocation.ARGS, Schema.Get)
    @jwt_required
    def get(self):
        """
        게시글 목록 API
        """

        session = main_db.session
        payload: self.Schema.Get = context_property.request_payload_object

        return {
            'data': [
                post.json_for_list for post in TblPosts.get_all(session, TblPosts.category_id == payload.category_id)
            ]
        }


class PostItemAPI(BaseResource):
    class Schema:
        class Patch(BaseModel):
            title = PostAPI.Schema.Post.title
            content = PostAPI.Schema.Post.content

    def get(self, post_id):
        """
        게시글 내용 조회 API
        """

        session = main_db.session

        post = TblPosts.get_post_object_through_id(session, post_id)

        return {
            'data': post.json_for_detail
        }

    @validate_with_schematics(PayloadLocation.JSON, Schema.Patch)
    @jwt_required
    def patch(self, post_id):
        """
        게시글 수정 API
        """

        payload: self.Schema.Patch = context_property.request_payload_object
        session = main_db.session
        user = context_property.requested_user

        TblPosts.update_post_with_permission_check(session, post_id, user, payload.title, payload.content)

        return {}

    @jwt_required
    def delete(self, post_id):
        """
        게시글 삭제 API
        """

        session = main_db.session
        user = context_property.requested_user

        TblPosts.delete_post_with_permission_check(session, post_id, user)

        return {}
