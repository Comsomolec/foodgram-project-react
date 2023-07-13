from rest_framework.exceptions import APIException


class CustomValidation(APIException):
    status_code = 400
    default_detail = 'Message'
