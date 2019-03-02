from flask import g


class _ContextProperty:
    @property
    def request_payload_object(self):
        return g.request_payload_object

    @request_payload_object.setter
    def request_payload_object(self, value):
        g.request_payload_object = value


context_property = _ContextProperty()
