import json
from json.decoder import JSONDecodeError


def get_data_from_request(request):

    if request.content_type == 'application/json':
        try:
            return json.loads(request.body.decode())
        except JSONDecodeError:
            return {"error": "no data in request"}

    else:
        return request.POST
