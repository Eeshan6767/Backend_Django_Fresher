import requests, json
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from ..checkers.requestChecker import RequestChecker
from ..checkers.exceptions import Wrong_HTTP_Method, Bad_JSON_Body, JSON_Decode_Error
from .utility import header

POST = 'POST'
WHATSAPP_FIELDS = {'to', 'from', 'body'}

class WhatsappAPI(View):

    @staticmethod
    def post(request) :  
        """
        This method handles whatsapp requests :
        1. Accepts post request from frontend. Mandatory Recieved data :
            In Data :               In Headers :
                - to number             - type :
                - from number           - api-key :
                - message content
        2. Converts it into Json
        3. Prepares a json body for making a post request to Kaleyra API endpoint
        4. Recieves the response from Kaleyra and sends it back to frontend
        
        
        Response body recieved from Kaleyra :
        {
            "id": "cc8074ae-990d-40f5-b604-11XXX9e2ab32",
            "type": "text",
            "body": "Hi, your order has been shipped",
            "createdDateTime": "2020-01-29 06:22:21+00:00",
            "totalCount": 1,
            "data": [
                {
                    "message_id": "cc8074ae-990d-40f5-b604-115XXXe2ab32:0",
                    "recipient": "1202XXXXXXX"
                }
            ],
            "error": {}
        }
        """ 
        try:
            RequestChecker.check(request, POST, WHATSAPP_FIELDS)
        except Wrong_HTTP_Method as err:
            return JsonResponse({'error' : err.message})
        except JSON_Decode_Error as err:
            return JsonResponse({'error' : err.message})
        except Bad_JSON_Body as err:
            return JsonResponse({'error' : err.message})
        
        json_body = json.loads(request.body)
        postData = {
            'to' : json_body.get('to'),
            'type' : "text",
            'channel' : "whatsapp",
            'from' : json_body.get('from'),
            'body' : json_body.get('body')
        }

        try :
            post_response = requests.post(url=settings.URL, json=postData, headers=header())
        except ValueError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=500, json=True)

        return JsonResponse(post_response.json())