from typing import Optional
from fastapi import APIRouter, Request, Depends, Query
from api.routers import STATISTICS_TASK
from consumer.data.response import ResponseApiData, Error
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.tasks.statistics import handler_get_task_statistics_task
from datetime import datetime
from django.utils import timezone

router = APIRouter()


@router.get(STATISTICS_TASK, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def get_task_statistics_task(
        request: Request,
        start_date: Optional[datetime] = Query(None, description="Start date of the statistics (format: yyyy-mm-dd)"),
        end_date: Optional[datetime] = Query(None, description="End date of the statistics (format: yyyy-mm-dd)")
):
    if not start_date:
        start_date = timezone.now()
    if not end_date:
        end_date = timezone.now()

    response = handler_get_task_statistics_task(start_date, end_date)
    if not response['is_valid']:
        return ResponseApiData(
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        ).to_response()

    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
