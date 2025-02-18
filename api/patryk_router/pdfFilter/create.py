import os
import time
from fastapi import APIRouter, Request, Depends, UploadFile, File, BackgroundTasks, WebSocket
from fastapi.responses import FileResponse
from api.routers import CREATE_PDF
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.patryk.pdfFilter.create import handler_create_pdf_filter
from consumer.helper.files import save_files_tmp
from consumer.helper.files import check_files_size
from consumer.services.patryk.pdfFilter.file import clear_catalog
from config.app_config import DOWNLOAD
from consumer.services.websocekt.patryk_router.pdfFilter.websocket import websocket_endpoint, send_progress
from consumer.helper.headers import check_required_headers

router = APIRouter()


@router.websocket("/ws/progress/{client_id}")
async def websocket_proxy(websocket: WebSocket, client_id: str):
    await websocket_endpoint(websocket, client_id)


@router.post(CREATE_PDF, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def create_pdf_filter(request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    if not file.filename.lower().endswith(".xlsx"):
        return ResponseApiData(
            status="ERROR",
            data="Typ file is not .xlsx!",
            status_code=400,
            additional=None
        ).to_response()

    files = [file]

    user_data = data_header['data'][0]['data']
    if check_files_size(files) > 0:
        save_files_tmp(files)
    else:
        return ResponseApiData(
            status="ERROR",
            data="File size is 0!",
            status_code=400,
            additional=None
        ).to_response()

    response = handler_create_pdf_filter(user_data)
    if response['is_valid'] and response['status'] == "SUCCESS":
        file_path = response['data']
        if file_path and os.path.exists(file_path):
            background_tasks.add_task(clear_catalog, DOWNLOAD)
            return FileResponse(path=file_path, media_type=str("application/pdf"),
                                headers={"Content-Disposition": f'attachment; filename="products.pdf"'})

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
