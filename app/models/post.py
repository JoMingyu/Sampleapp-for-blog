from flask import abort
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.user import TblUsers


class TblPosts(Base):
    __tablename__ = 'tbl_posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String(5000))
    owner_id = Column(String(256), ForeignKey('tbl_users.id'))
    category_id = Column(Integer, ForeignKey('tbl_categories.id'))

    owner = relationship('TblUsers')
    category = relationship('TblCategories')

    @property
    def json_for_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'ownerNickname': self.owner.nickname
        }

    @property
    def json_for_detail(self):
        return {
            'content': self.content
        }

    @classmethod
    def get_post_object_through_id(cls, read_session, id: int) -> 'TblPosts':
        post = cls.get_first_or_abort_on_none(read_session, cls.id == id)

        return post

    @classmethod
    def get_post_object_through_id_with_permission_check(
        cls, read_session, id: int, requested_user: TblUsers
    ) -> 'TblPosts':
        post = cls.get_post_object_through_id(read_session, id)

        if post.owner_id != requested_user.id:
            abort(403)

        return post

    @classmethod
    def update_post_with_permission_check(cls, write_session, id: int, requested_user: TblUsers, title, content):
        post = cls.get_post_object_through_id_with_permission_check(write_session, id, requested_user)

        post.title = title
        post.content = content

        write_session.add(post)
        write_session.commit()

    @classmethod
    def delete_post_with_permission_check(cls, write_session, id: int, requested_user: TblUsers):
        post = cls.get_post_object_through_id_with_permission_check(write_session, id, requested_user)

        write_session.delete(post)
        write_session.commit()
