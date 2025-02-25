from consumer.data.response import ResponseData
from consumer.data.user import UserData
from consumer.services.patryk.pdfFilter.file import open_file_xlsx, extract_images_from_xlsx, clear_tmp_files, \
    clear_catalog
from config.app_config import AUTO_REMOVE_FILES
from consumer.services.patryk.pdfFilter.sum import sum_duplicat
from consumer.services.patryk.pdfFilter.convert import convert_product_with_images
from consumer.services.patryk.pdfFilter.pdf import generate_pdf
from config.app_config import FILE
from consumer.services.websocekt.patryk_router.pdfFilter.websocket import send_progress


def handler_create_pdf_filter(user: UserData) -> ResponseData:
    try:
        send_progress(user['id'], 10, "Rozpoczecie sciagania plikow z pliku .xlsx...")
        images, err, is_valid = extract_images_from_xlsx()
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data={
                    'type': 'extract_images_from_xlsx',
                    'error': err
                },
                status_code=400,
                additional=None
            )

        send_progress(user['id'], 20, "Otwarcie pliku .xlsx...")
        data_open_file, err, is_valid = open_file_xlsx()
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data={
                    'type': 'open_file_xlsx',
                    'error': err
                },
                status_code=400,
                additional=None
            )

        send_progress(user['id'], 30, "Sumowanie duplikatow...")
        sum_data, err, is_valid = sum_duplicat(data_open_file)
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data={
                    'type': 'sum_duplicat',
                    'error': err
                },
                status_code=400,
                additional=None
            )

        send_progress(user['id'], 40, "Przypiswanie zdjec do poszegolnych obiektow...")
        full_products, err, is_valid = convert_product_with_images(sum_data, images)
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data={
                    'type': 'convert_product_with_images',
                    'error': err
                },
                status_code=400,
                additional=None
            )

        send_progress(user['id'], 50, "Generowanie pdfa...")
        err_or_path, is_valid = generate_pdf(user['id'], full_products, "products.pdf")
        send_progress(user['id'], 60, "Pdf zostal utworzony...")
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data={
                    'type': 'generate_pdf',
                    'error': err_or_path
                },
                status_code=400,
                additional=None
            )

        send_progress(user['id'], 70, "Rozpoczecie czyszczenia plikow...")
        if AUTO_REMOVE_FILES:
            path_files = []
            for path in images:
                path_files.append(path['url_image'])

            clear_tmp_files(path_files)
            clear_catalog(FILE)
        send_progress(user['id'], 80, "Zakonczenie procesu z pdfem!")

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=str(err_or_path),
            status_code=200,
            additional=None
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
