from consumer.data.patryk.pdfFilter.product import ProductData


def sum_duplicat(products: list[ProductData]) -> tuple[list[dict], str, bool]:
    try:

        summed_products = {}

        for product in products:

            name = product['name']
            quantity = int(product['quantity'])

            if name in summed_products:
                summed_products[name]['quantity'] += quantity
            else:
                summed_products[name] = {
                    'column_excel': product['column_excel'],
                    'lp': product['lp'],
                    'name': name,
                    'quantity': quantity,
                    'ean': product['ean'],
                    'location': product['location'],
                }
        result = list(summed_products.values())
        for i, item in enumerate(result, start=1):
            item['index'] = i
        return result, "", True

    except Exception as e:
        return [], str(e), False
