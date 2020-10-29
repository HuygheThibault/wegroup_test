class FormattedException(Exception):
    def __init__(self, msg, domain=None, detail=None, code=None, formatted=False):
        if hasattr(msg, "args"):
            msg = msg.args

        super().__init__(msg)
        self.domain = domain
        self.detail = detail
        self.code = code
        self.msg = msg

    @property
    def formatted(self):
        return {"msg": self.msg, "domain": self.domain, "detail": self.detail, "code": self.code}


class TooManyRequestsException(FormattedException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.code = 429
        self.msg = "TOO_MANY_REQUESTS"
        self.detail = detail
