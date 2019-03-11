from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class TblCategories(Base):
    __tablename__ = 'tbl_categories'

    id = Column(Integer, primary_key=True)
    # SQLAlchemy가 첫 integer 타입의 PK에 auto increment 속성을 알아서 부여함
    name = Column(String(32), unique=True)
    author_id = Column(String(256), ForeignKey('tbl_users.id'))

    author = relationship('TblUsers')

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
