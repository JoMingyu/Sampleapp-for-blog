from flask_jwt_extended import jwt_refresh_token_required, create_access_token

from app.context import context_property
from app.views.base import BaseResource


class RefreshAPI(BaseResource):
    @jwt_refresh_token_required
    def get(self):
        """
        Access token refresh API
        """
        user = context_property.requested_user

        return {
            'accessToken': create_access_token(user.id)
        }, 200
