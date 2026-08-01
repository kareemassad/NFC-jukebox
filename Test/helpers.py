class HttpError(Exception):
    def __init__(self, http_status):
        super().__init__(f"HTTP {http_status}")
        self.http_status = http_status
