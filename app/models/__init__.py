from abc import abstractmethod
from typing import Union

from flask import abort, g, has_request_context
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.elements import ClauseElement

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

    @classmethod
    def get_first_without_none_check(cls, read_session: Session, where_clause: Union[ClauseElement, bool]):
        """
        전달된 session을 통해 cls에 대해 where_caluse로 필터해 쿼리하고, None 여부에 상관없이 .first()의 결과를 리턴합니다.
        """
        return read_session.query(cls).filter(where_clause).first()

    @classmethod
    def get_first_or_abort_on_none(cls, read_session: Session, where_clause: Union[ClauseElement, bool], code=404, message: str=None):
        """
        1. 전달된 session을 통해 cls에 대해 where_caluse로 필터해 쿼리하고
        2. .first() 후 결과가 None이면 인자 정보들을 통해 abort,
        3. None이 아니라면 해당 객체를 리턴
        """
        res = cls.get_first_without_none_check(read_session, where_clause)

        if res is None:
            abort(code, message)
        else:
            return res

    @classmethod
    def delete(cls, write_session: Session, where_clause: Union[ClauseElement, bool]):
        """
        전달된 session을 통해 cls에 대해 where_clause로 필터해 쿼리하고, 결과를 모두 delete합니다.
        commit을 수행하지 않음에 주의하기 바랍니다.
        """
        write_session.query(cls).filter(where_clause).delete()

    @classmethod
    def delete_and_commit(cls, write_session: Session, where_clause: Union[ClauseElement, bool]):
        """
        where_clause를 통해 delete 후, commit까지 수행합니다.
        """
        cls.delete(write_session, where_clause)
        write_session.commit()


class DB:
    @abstractmethod
    def extract_create_engine_kwargs(self, flask_app) -> dict:
        """
        `self.checkout_new_session`을 초기화하기 위해 호출하는
        `sqlalchemy.create_app` 함수에 전달할 인자들을 dictionary로 반환합니다.
        """

        pass

    @property
    @abstractmethod
    def attribute_name_on_g(self) -> str:
        """
        g 객체에 session 객체를 저장할 때 사용할 attribute name입니다.
        setattr(obj, name, value)에서 `name` 자리에 사용됩니다.
        """

        pass

    @property
    def session(self) -> Session:
        """
        g 객체에서 session 객체를 가져와 반환합니다.
        현재 context에 대해 checkout된 session이 없으며 request context가 활성화되어 있는 경우, 새로 생성합니다.
        """

        session = getattr(g, self.attribute_name_on_g, None)

        if session is None and has_request_context():
            session = self.checkout_new_session()
            setattr(g, self.attribute_name_on_g, session)

        return session

    @session.setter
    def session(self, value: Session):
        """
        g 객체에 session 객체를 저장합니다.
        """

        setattr(g, self.attribute_name_on_g, value)

    def __init__(self, flask_app=None):
        self.engine = None
        self.checkout_new_session = None

        if flask_app is not None:
            self.init_app(flask_app)

    def init_app(self, flask_app):
        self.engine = create_engine(**self.extract_create_engine_kwargs(flask_app))
        self.checkout_new_session = sessionmaker(self.engine)

        @flask_app.teardown_appcontext
        def teardown_request(_):
            """
            context에 대해 session이 한 번 이상 checkout되었다면 이를 close해주기 위한 teardown callback
            """

            session = self.session

            if session is not None:
                session.close()


class MainDB(DB):
    def extract_create_engine_kwargs(self, flask_app):
        return {
            'name_or_url': flask_app.config['MAIN_DB_URL']
        }

    @property
    def attribute_name_on_g(self):
        return 'main_db_session'
