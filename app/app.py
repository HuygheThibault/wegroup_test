from __future__ import absolute_import

from app.app_factory import create_app
from app.config import Config

app = create_app(Config())
