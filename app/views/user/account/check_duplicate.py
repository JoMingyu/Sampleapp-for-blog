from flask import abort

from app.extensions import main_db
from app.models.user import TblUsers
from app.views.base import BaseResource


class IDDuplicateCheckAPI(BaseResource):
    def get(self, id):
        """
        ID 중복체크 API
        """

        session = main_db.session

        if TblUsers.is_id_already_signed(session, id):
            abort(409)
        else:
            return {}, 200
