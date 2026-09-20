from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.guarantees import collection_expiring_guarantees_psql
from core.repository.psql.file.response import RepositoryCollectionFileResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_expiring_guarantees(
    user_id: str,
    limit: int = 32,
    offset: int = 0,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_expiring_guarantees_psql(limit=limit, offset=offset, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:guarantees_expiring", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_expiring_guarantees",
            type_error="exception",
            key_type_error="Exception",
        ), False
