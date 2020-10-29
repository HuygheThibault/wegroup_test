from __future__ import absolute_import
from enum import Enum

from pydantic import Field, conint, constr

from .base import Base


class error_enum_401(Enum):
    AUTHENTICATION_EXPIRED = "AUTHENTICATION_EXPIRED"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    ENVIRONMENT_MISMATCH = "ENVIRONMENT_MISMATCH"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    REFRESH_TOKEN_INCORRECT = "REFRESH_TOKEN_INCORRECT"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
    USER_BLACKLISTED = "USER_BLACKLISTED"


class rate_limit_error_msg_enum(Enum):
    RATE_LIMIT = "RATE_LIMIT"


class server_error_msg_enum(Enum):
    SERVER_ERROR = "SERVER_ERROR"


ErrorDetail = constr(min_length=2, max_length=1000, strip_whitespace=True)
ErrorMsg = constr(min_length=3, max_length=100, regex=r"^[A_Z0-9_]+$", strip_whitespace=True)


class Error_4XX(Base):
    """
    Error 4XX
    """

    msg: ErrorMsg = Field(..., description="The key describing the error.", example="USER_NOT_FOUND")
    detail: ErrorDetail = Field(
        ..., description="A detail describing the error.", example="A username should not contain special characters."
    )
    code: conint(ge=400, lt=500) = Field(..., description="The error code.", example=404)
    domain: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        None, description="The domain details.", example="authentication"
    )


class Error_403(Base):
    """
    Error 403
    Authorization error.
    """

    detail: ErrorDetail = Field(
        ..., description="A detail describing the error.", example="A username should not contain special characters."
    )
    msg: ErrorMsg = Field(
        ...,
        description="The key describing the error, this is very important and is used for checking.",
        example="NOT_AUTHORIZED",
    )
    code: conint(ge=403, lt=403) = Field(403, description="The error code.", example=403)
    domain: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        None, description="The domain details.", example="authentication"
    )


class Error_401(Base):
    """
    Error 401
    Authentication error.
    """

    msg: error_enum_401 = Field(
        ...,
        description="The key describing the error, this is very important and is used for checking.",
        example="AUTHENTICATION_EXPIRED",
    )
    detail: ErrorDetail = Field(
        ..., description="A detail describing the error.", example="A username should not contain special characters."
    )
    code: conint(ge=401, lt=401) = Field(401, description="The error code.", example=401)
    domain: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        None, description="The domain details.", example="authentication"
    )


class Error_429(Base):
    """
    Error 429
    Rate limit error.
    """

    msg: rate_limit_error_msg_enum = Field(
        ...,
        description="The key describing the error, this is very important and is used for checking.",
        example="RATE_LIMIT",
    )
    detail: ErrorDetail = Field(
        ..., description="A detail describing the error.", example="A username should not contain special characters."
    )
    code: conint(ge=429, lt=429) = Field(429, description="The error code.", example=429)
    domain: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        None, description="The domain details.", example="authentication"
    )


class Error_500(Base):
    """
    Error 500
    Server error.
    """

    msg: server_error_msg_enum = Field(
        ...,
        description="The key describing the error, this is very important and is used for checking.",
        example="SERVER_ERROR",
    )
    detail: ErrorDetail = Field(
        ..., description="A detail describing the error.", example="A username should not contain special characters."
    )
    code: conint(ge=500, lt=500) = Field(500, description="The error code.", example=500)
    domain: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        None, description="The domain details.", example="authentication"
    )
