from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class TblComments(Base):
    __tablename__ = 'tbl_comments'

    id = Column(Integer, primary_key=True)
    content = Column(String(500))
    owner_email = Column(String(256), ForeignKey('tbl_users.email'))
    post_id = Column(Integer, ForeignKey('tbl_posts.id'))

    owner = relationship('TblUsers')
    post = relationship('TblPosts')
