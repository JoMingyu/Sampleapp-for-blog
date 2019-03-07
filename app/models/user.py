from sqlalchemy import Column, String, CHAR

from app.models import Base


class TblUsers(Base):
    __tablename__ = 'tbl_users'

    id = Column(String(64), primary_key=True)
    password = Column(CHAR(93))  # len(werkzeug.security.generate_password_hash())
    nickname = Column(String(32))

    @classmethod
    def is_id_already_signed(cls, session, id):
        return cls.get_first_without_none_check(session, cls.id == id) is not None
