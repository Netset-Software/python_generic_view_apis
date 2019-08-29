from functools import wraps
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


def login_required(view_func):

    def _decorator(request, *args, **kwargs):
        try:
            # maybe do something before the view_func call
            api_key = request.META.get('HTTP_AUTHORIZATION')
            token1 = Token.objects.get(key=api_key)
            user = token1.user
            check_group = user.groups.filter(name='Admin').exists()
            if check_group == False:
                return JsonResponse({"message" : "Login required.", "status":"0"}, status=401)
            
            response = view_func(request, *args, **kwargs)
            return response
        except Exception:
            return JsonResponse({"message" : "Login required.", "status":"0"}, status=401)

    return wraps(view_func)(_decorator)

