from flask_jwt_extended import jwt_refresh_token_required, create_access_token, get_jwt_identity

from app.extensions import main_db
from app.models.user import TblUsers
from app.views.base import BaseResource


class RefreshAPI(BaseResource):
    @jwt_refresh_token_required
    def get(self):
        """
        Access token refresh API
        """

        session = main_db.session
        identity = get_jwt_identity()

        user: TblUsers = TblUsers.get_first_or_abort_on_none(
            session,
            TblUsers.id == identity,
            code=401
        )

        return {
            'accessToken': create_access_token(user.id)
        }, 201
