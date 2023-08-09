from django.views import View
from django.http import JsonResponse
from django.conf import settings

import json, requests
from ..checkers.requestChecker import RequestChecker
from ..checkers.exceptions import Wrong_HTTP_Method, Bad_JSON_Body, JSON_Decode_Error
from myApp.models import Flag
from .utility import header

POST = 'POST'
URL_FIELDS = {'url'}

class ShortenURL(View):

    @staticmethod
    def post(request):

        """
            Handling URL Shortning request.
            Request body contains data in JSON format.
                -url
            These key-value pairs are generated from https://pp-in.kaleyra.io/developers/ and take reference from Kaleyra Developers documentation https://developers.kaleyra.io/docs
            Response body will have the short-url as
            {
                "url": "https://txtly-pp.kaleyra.io/zoE"
            }
        """ 
        
        try:
            RequestChecker.check(request, POST, URL_FIELDS)
        except Wrong_HTTP_Method as err:
            return JsonResponse({'error' : err.message})
        except JSON_Decode_Error as err:
            return JsonResponse({'error' : err.message})
        except Bad_JSON_Body as err:
            return JsonResponse({'error' : err.message})

        json_body = json.loads(request.body)

        try:
            result = requests.post(f'{settings.BASEURL}/url-shortner', json=json_body, headers=header())
        except requests.exceptions.RequestException as err:
            return JsonResponse({"err" : "There is some issue please try later."})
        return JsonResponse(result.json())