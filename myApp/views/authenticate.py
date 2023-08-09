import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

from ..models import User, Flag
from ..checkers.requestChecker import RequestChecker
from ..checkers.exceptions import Wrong_HTTP_Method, Bad_JSON_Body, UserAlreadyExists, JSON_Decode_Error

POST = 'POST'
GET = 'GET'
REGISTER_FIELDS = {'user_name', 'user_password', 'user_email'}
LOGIN_FIELDS = {'user_name', 'user_password'}
ENTRY_SUCCESSFUL_FIELDS = {'user_name'}


class CreateUser:

    def __init__(self, name, password, email):
        """
        the constuctor tries to create a user record and corresponsding flag record
            - if a user with same user name exists, an error is raised with proper message
            - failure in any of the records creation, error with proper message is raised
        """
        if CreateUser.user_exists(name)==None:
            encrypted_pwd = make_password(password)
            flag_data = {
                'sms' : False,
                'whatsapp' : False,
                'url_shortner' : False
            }

            try :
                new_user = User.objects.create(user_name = name, user_password = encrypted_pwd, user_email = email)
            except IntegrityError as err:
                raise IntegrityError(f'Could not register User - Integrity Error')
            try :
                new_flag = Flag.objects.create(user_id = new_user, user_flags = flag_data)
            except IntegrityError as err:
                raise IntegrityError(f'Could not create Flag for User - Integrity Error')
        else :
                raise UserAlreadyExists("The user_name is already taken! Choose a different user_name")

    @staticmethod
    def user_exists(name):
        try :
            checkUser = User.objects.get(user_name = name)
        except User.DoesNotExist:
            return None
        return checkUser


class Register(View):

    @staticmethod
    def post(request):
        """
        function for registering user in the database
            - if success: it will respond with proper message, status code and user name
            - if failed: it will send respond with an mesaage that registration could not be done
            - if user already exists, a reponse with that user already exists, try to login
        """
        try:
            RequestChecker.check(request, POST, REGISTER_FIELDS)
        except Wrong_HTTP_Method as err:
            return JsonResponse({'error' : err.message})
        except JSON_Decode_Error as err:
            return JsonResponse({'error' : err.message})
        except Bad_JSON_Body as err:
            return JsonResponse({'error' : err.message})

        json_body = json.loads(request.body)
        name = json_body.get('user_name')
        password = json_body.get('user_password')
        email = json_body.get('user_email')

        try:
            new_user = CreateUser(name, password, email)
        except IntegrityError as  err:
            return JsonResponse({'error' : err.args[0]}, status = 500)
        except UserAlreadyExists as err:
            return JsonResponse({'error' : err.message}, status = 500)
        
        return JsonResponse( {'message' : 'Registration successful', 'user_name' : name}, status = 200)


class Login(View):

    @staticmethod
    def post(request):
        try:
            RequestChecker.check(request, POST, LOGIN_FIELDS)
        except Wrong_HTTP_Method as err:
            return JsonResponse({'error' : err.message})
        except JSON_Decode_Error as err:
            return JsonResponse({'error' : err.message})
        except Bad_JSON_Body as err:
            return JsonResponse({'error' : err.message})
        
        json_body = json.loads(request.body)
        name = json_body.get('user_name')
        password = json_body.get('user_password')
        checkUser = CreateUser.user_exists(name)

        if checkUser==None:
            return JsonResponse( {'message' : "You're not registered"}, status = 404)
        else : 
            if check_password(password, checkUser.user_password):
                return JsonResponse( {'message' : 'Login Successful!', 'user_name' : name}, status = 200)
            else:
                return JsonResponse( {'message' : 'Incorrect Password!'}, status = 401)


class EntrySuccessful(View):

    @staticmethod
    def get(request):
        # try:
        #     RequestChecker.check(request, GET, ENTRY_SUCCESSFUL_FIELDS)
        # except Wrong_HTTP_Method as err:
        #     return JsonResponse({'error' : err.message})
        # except Bad_JSON_Body as err:
        #     return JsonResponse({'error' : err.message})
        
        try:
            userInfo=User.objects.get(user_name = request.GET.get('user_name'))
        except User.DoesNotExist as e :
            return JsonResponse( {'message' : str(e)}, status = 404)
        try:
            userFlags = Flag.objects.get(user_id = userInfo.user_id)
        except Flag.DoesNotExist as e :
            return JsonResponse( {'message' : str(e)}, status = 404)
        
        data = {
            'user_data' : {
                'user_name' : userInfo.user_name,
                'user_email' : userInfo.user_email,
                'user_balance' : userInfo.user_balance,
            },
            'user_flags' : {
                'sms' : userFlags.user_flags['sms'],
                'whatsapp' : userFlags.user_flags.get('whatsapp', False),
                'url_shortner' : userFlags.user_flags['url_shortner']
            } 
        }

        return JsonResponse(data)