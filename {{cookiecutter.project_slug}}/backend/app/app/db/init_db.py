import logging

from app.core.config import (
    COUCHBASE_PASSWORD,
    COUCHBASE_USER,
    COUCHBASE_HOST,
    COUCHBASE_PORT,
    COUCHBASE_BUCKET_NAME,
    FIRST_SUPERUSER,
    FIRST_SUPERUSER_PASSWORD,
    COUCHBASE_SYNC_GATEWAY_USER,
    COUCHBASE_SYNC_GATEWAY_PASSWORD,
)
from app.db.couchbase_utils import config_couchbase
from app.db.database import (
    ensure_create_bucket,
    get_bucket,
    ensure_create_primary_index,
    ensure_create_type_index,
    ensure_create_couchbase_app_user,
)
from app.crud.user import upsert_user
from app.models.role import RoleEnum
from app.models.user import UserInCreate


def init_db():
    logging.info("before config_couchbase")
    config_couchbase(
        COUCHBASE_USER, COUCHBASE_PASSWORD, host=COUCHBASE_HOST, port=COUCHBASE_PORT
    )
    logging.info("after config_couchbase")
    # COUCHBASE_USER="Administrator"
    # COUCHBASE_PASSWORD="password"
    logging.info("before ensure_create_bucket")
    ensure_create_bucket(
        COUCHBASE_USER,
        COUCHBASE_PASSWORD,
        COUCHBASE_BUCKET_NAME,
        host=COUCHBASE_HOST,
        port=COUCHBASE_PORT,
    )
    logging.info("after ensure_create_bucket")
    logging.info("before get_bucket")
    bucket = get_bucket(
        COUCHBASE_USER,
        COUCHBASE_PASSWORD,
        COUCHBASE_BUCKET_NAME,
        host=COUCHBASE_HOST,
        port=COUCHBASE_PORT,
    )
    logging.info("after get_bucket")
    logging.info("before ensure_create_primary_index")
    ensure_create_primary_index(bucket)
    logging.info("after ensure_create_primary_index")
    logging.info("before ensure_create_type_index")
    ensure_create_type_index(bucket)
    logging.info("after ensure_create_type_index")
    logging.info("before ensure_create_couchbase_app_user sync")
    ensure_create_couchbase_app_user(
        COUCHBASE_USER,
        COUCHBASE_PASSWORD,
        COUCHBASE_SYNC_GATEWAY_USER,
        COUCHBASE_SYNC_GATEWAY_PASSWORD,
        COUCHBASE_BUCKET_NAME,
        host=COUCHBASE_HOST,
        port=COUCHBASE_PORT,
    )
    logging.info("after ensure_create_couchbase_app_user sync")
    logging.info("before upsert_user first superuser")
    in_user = UserInCreate(
        name=FIRST_SUPERUSER,
        password=FIRST_SUPERUSER_PASSWORD,
        email=FIRST_SUPERUSER,
        admin_roles=[RoleEnum.superuser, RoleEnum.admin],
        admin_channels=[FIRST_SUPERUSER, RoleEnum.admin],
    )
    upsert_user(
        bucket,
        in_user
    )
    logging.info("after upsert_user first superuser")
