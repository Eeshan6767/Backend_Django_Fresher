from .exceptions import Wrong_HTTP_Method, Bad_JSON_Body, JSON_Decode_Error
import json


class RequestChecker:

    @staticmethod
    def check(request, type, required_fields):
        """
        this method is for checking the request, 2 critreria :
            - type_error : request method dosen't match the type
            - header error : 
            - body error :  report missing fields
                            report uneccessary extra fields
        appropriate errors will be raised
        """
        if request.method != type:
            raise Wrong_HTTP_Method(f'Expected : {type}, recieved : {request.method}')
        
        try:
            json_body = json.loads(request.body)
        except json.JSONDecodeError:
            raise JSON_Decode_Error('JSON_Decode_Error : Invalid JSON Payload')
        
        available_fields = set()
        for key in json_body :
            available_fields.add(key)
        missing_fields = required_fields - available_fields
        extra_fields = available_fields - required_fields

        if(len(missing_fields)!=0):
            raise Bad_JSON_Body(f'missng the following fileds : {missing_fields}')
        if(len(extra_fields)!=0):
            raise Bad_JSON_Body(f'Data Overload-Extra fields : {extra_fields}')