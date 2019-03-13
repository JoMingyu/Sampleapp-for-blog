from flask import g
from flask_jwt_extended import get_jwt_identity

from app.extensions import main_db
from app.models.user import TblUsers


class _ContextProperty:
    @property
    def request_payload_object(self):
        return g.request_payload_object

    @request_payload_object.setter
    def request_payload_object(self, value):
        g.request_payload_object = value

    @property
    def requested_user(self) -> TblUsers:
        requested_user = getattr(g, 'requested_user', None)

        if requested_user:
            return requested_user
        else:
            session = main_db.session

            user = TblUsers.get_first_or_abort_on_none(
                session,
                TblUsers.id == get_jwt_identity(),
                code=401
            )

            g.requested_user = user

            return user


context_property = _ContextProperty()
