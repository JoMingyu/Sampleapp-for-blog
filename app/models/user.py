from sqlalchemy import Column, String, CHAR

from app.models import Base


class TblUsers(Base):
    __tablename__ = 'tbl_users'

    email = Column(String(256), primary_key=True)  # RFC 5321
    password = Column(CHAR(93))  # len(werkzeug.security.generate_password_hash())
    nickname = Column(String(32))
