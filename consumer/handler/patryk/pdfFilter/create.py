from consumer.data.response import ResponseData
from consumer.services.patryk.pdfFilter.file import open_file_xlsx, extract_images_from_xlsx, clear_tmp_files, \
    clear_catalog
from config.app_config import AUTO_REMOVE_FILES
from consumer.services.patryk.pdfFilter.sum import sum_duplicat
from consumer.services.patryk.pdfFilter.convert import convert_product_with_images
from consumer.services.patryk.pdfFilter.pdf import generate_pdf
from config.app_config import FILE


def handler_create_pdf_filter() -> ResponseData:
    try:
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

        err_or_path, is_valid = generate_pdf(full_products, "products.pdf")
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

        if AUTO_REMOVE_FILES:
            path_files = []
            for path in images:
                path_files.append(path['url_image'])

            clear_tmp_files(path_files)
            clear_catalog(FILE)

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
