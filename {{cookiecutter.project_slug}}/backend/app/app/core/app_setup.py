# Import standard library packages

# Import installed packages
from raven.contrib.flask import Sentry

# Import app code
from app.main import app
from app.db.bucket import bucket
from app.core import config
from app.core.config import (
    COUCHBASE_USER,
    COUCHBASE_PASSWORD,
    COUCHBASE_BUCKET_NAME,
    COUCHBASE_HOST,
    COUCHBASE_PORT,
)

# Set up CORS
from . import cors  # noqa

from .jwt import jwt  # noqa
from . import errors  # noqa

from ..api.api_v1 import api as api_v1  # noqa

app.config["SECRET_KEY"] = config.SECRET_KEY
# app.config["JWT_ALGORITHM"] = "RS256"

sentry = Sentry(app, dsn=config.SENTRY_DSN)
