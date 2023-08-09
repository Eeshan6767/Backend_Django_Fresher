from django.views import View
from django.http import JsonResponse
from django.conf import settings

from ..checkers.requestChecker import RequestChecker
from ..checkers.exceptions import Wrong_HTTP_Method, Bad_JSON_Body, JSON_Decode_Error

import requests, json
from .utility import header

POST = 'POST'
SMS_FIELDS = {'to', 'type', 'body', 'source'}

class SMS(View):

    @staticmethod
    def post(request):

        """
            Handling SMS request.
            Request body contains data in JSON format.
                - to 
                - type
                - body
                - source
            Two fields then added to the data then passed toKaleyra's API and the response get returned to client.
                - sender
                - template_id
            These key-value pairs are generated from https://pp-in.kaleyra.io/developers/ and take reference from Kaleyra Developers documentation https://developers.kaleyra.io/docs
            Response body will have the data as
            {
                "id": "ee8aXXXX-XXXX-XXXX-XXXX-9b717XXXX30d",
                "sender": "KLRHXA",
                "type": "DEFAULT",
                "body": "Hello! This is my first SMS.",
                "createdDateTime": "2019-11-04 10:42:23+00:00",
                "totalCount": 1,
                "data": [
                    {
                    "message_id": "ee8aXXXX-XXXX-XXXX-XXXX-9b717XXXX30d:1",
                    "recipient": "1XXXXXXXXXX"
                    }
                ],
                "dlrurl": null,
                "error": {}
            }
        """ 
        
        try:
            RequestChecker.check(request, POST, SMS_FIELDS)
        except Wrong_HTTP_Method as err:
            return JsonResponse({'error' : err.message})
        except JSON_Decode_Error as err:
            return JsonResponse({'error' : err.message})
        except Bad_JSON_Body as err:
            return JsonResponse({'error' : err.message})

        body_json = json.loads(request.body)
        body_json["sender"] = "APITES"
        body_json["template_id"] = settings.TEMPLATE_ID

        try:
            result = requests.post(settings.URL, data=json.dumps(body_json), headers=header())
        except requests.exceptions.RequestException as err:
            return JsonResponse({"err" : "There is some issue please try later."})
        return JsonResponse(result.json())
