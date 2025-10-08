from core.data.patryk.pdfFilter.product import ProductData
from core.data.patryk.pdfFilter.image import ImageData


def convert_product_with_images(products: list[ProductData], images: list[ImageData]) -> tuple[list[dict], str, bool]:
    try:

        image_map = {image['index']: image['url_image'] for image in images}

        data = []
        for index, product in enumerate(products):
            new_object = {
                'index': product['index'],
                'column_excel': product['column_excel'],
                'lp': product['lp'],
                'name': product['name'],
                'quantity': product['quantity'],
                'ean': product['ean'],
                'url_image': image_map.get(product['index'], None),
                'location': product['location']
            }
            data.append(new_object)

        return data, "", True
    except Exception as e:
        return [], str(e), False
