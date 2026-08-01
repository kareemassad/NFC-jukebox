from types import SimpleNamespace


class HttpError(Exception):
    def __init__(self, http_status, message="", headers=None):
        super().__init__(message or f"HTTP {http_status}")
        self.http_status = http_status
        self.msg = message
        self.reason = message
        self.response = SimpleNamespace(
            status_code=http_status,
            headers=headers or {},
        )


class NoStatusError(Exception):
    pass
