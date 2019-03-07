from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class TblPosts(Base):
    __tablename__ = 'tbl_posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String(5000))
    owner_id = Column(String(256), ForeignKey('tbl_users.id'))
    category_id = Column(Integer, ForeignKey('tbl_categories.id'))

    owner = relationship('TblUsers')
    category = relationship('TblCategories')
