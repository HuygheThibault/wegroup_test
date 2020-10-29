from __future__ import absolute_import
from enum import Enum

from .base import Base


class ZipCodeRiskFactor(Enum):
    A = "A"
    B = "B"
    C = "C"


class ZipCodeRiskFactor(Base):
    zipcode: int
    risk_factor: ZipCodeRiskFactor
