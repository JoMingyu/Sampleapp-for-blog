from flask import request

from app.views.base import BaseResource


class Sample(BaseResource):
    def post(self):
        payload = request.json

        return payload, 201
