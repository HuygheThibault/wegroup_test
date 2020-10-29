from __future__ import absolute_import
from app.db.db import DB
from app.models.base import Base
from app.models.zipcode import ZipCodeRiskFactor


class ZipCodeRepository(Base):
    db: DB

    async def get(self, zipcode: int) -> ZipCodeRiskFactor:
        ...
