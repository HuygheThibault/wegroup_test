from __future__ import absolute_import

import asyncio
import logging

from fastapi import FastAPI

from app.api.endpoints.api import router
from app.config import Config
from app.db.db import DB
from app.models.session import Session, SessionWrapper
from app.repositories.zipcode import ZipCodeRepository


def create_app(config: Config):
    app = FastAPI(openapi_url="/openapi/spec.json", docs_url="/swagger", redoc_url="/redoc", debug=True)
    app.include_router(router)

    # wire things up
    app.config = Config()
    app.session = SessionWrapper(s=Session())
    app.db = DB(app.config.DB_DSN.get_secret_value())
    app.repositories = lambda: None
    app.repositories.zipcodes = ZipCodeRepository(db=app.db)
    app.shutdown = lambda: __import__('os').kill(app.config.PID, __import__('signal').SIGTERM)

    @app.on_event("startup")
    async def setup() -> None:
        logging.info(f"[APP_SETUP] {app} {app.config}")

        app.loop = asyncio.get_running_loop()
        await app.db.setup(app)
        await app.session.s.setup()

    @app.on_event("shutdown")
    async def teardown() -> None:
        logging.info(f"[APP_TEARDOWN] {app} {app.config}")

        await app.session.s.teardown()
        await app.db.teardown()

    return app
