from consumer.data.response import ResponseData, create_success_response, create_error_response
import json


def check_required_headers(request, required_headers) -> ResponseData:
    try:
        missing_headers = []
        data_header = []

        for header in required_headers:
            if not request.headers.get(header):
                missing_headers.append(header)

        if missing_headers:
            return create_error_response(message=f'Missing headers: {", ".join(missing_headers)}', status_code=403)

        for header in required_headers:
            if header == "UserData":
                try:
                    json_data = json.loads(request.headers.get(header))
                    data_header.append({
                        "header": header,
                        "data": json_data
                    })
                except json.JSONDecodeError as e:
                    return create_error_response(message=f'Invalid JSON format in header: {e}.', status_code=403)
            elif header == "X-Refresh-Token":
                data_header.append({
                    "header": header,
                    "data": request.headers.get(header)
                })

        return create_success_response(data=data_header, status_code=200)

    except Exception as e:
        return create_error_response(message=str(e), status_code=403)
