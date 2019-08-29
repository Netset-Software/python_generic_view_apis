from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from apis.models import Item, User
from apis.serializers import ItemSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
import traceback
from django.contrib.auth.hashers import make_password
from django.db import transaction
import json
from django.utils import timezone
from django.contrib.auth import authenticate

@api_view(['POST'])
def add_admin(request):
    try:
        with transaction.atomic():
            received_json_data = json.loads(request.body, strict=False)
            user = User.objects.create(username=received_json_data['username'],
                                 email=received_json_data['email'],
                                 first_name=received_json_data['first_name'],
                                 last_name=received_json_data['last_name'],
                                 password=make_password(received_json_data['password']),
                                 is_superuser=0,
                                 is_staff=0,
                                 is_active=1,
                                 date_joined=timezone.now(),
                                 zip=received_json_data['zip'],
                                 phone=received_json_data['phone'],
                                 address=received_json_data['address'],
                                 role=1)
            if user is not None:
                g = Group.objects.get(name='Admin')
                g.user_set.add(user)
                return Response({"message" : "Successfully added", "status" : "1"}, status=status.HTTP_201_CREATED)
                
            else:
                return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def login_admin_user(request):
    try:
        with transaction.atomic():
                received_json_data = json.loads(request.body, strict=False)
                username = received_json_data['username']
                password = received_json_data['password']
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    checkGroup = user.groups.filter(name='Admin').exists()
                    if checkGroup:
                        if user.is_active == 1:
                            token = ''
                            try:
                                user_with_token = Token.objects.get(user=user)
                            except:
                                user_with_token = None
                            
                            if user_with_token is None:
                                token1 = Token.objects.create(user=user)
                                token = token1.key
                            else:
                                Token.objects.get(user=user).delete()
                                token1 = Token.objects.create(user=user)
                                token = token1.key
                            
                            return Response({"status" : "1", "token" : token, "message":"Login successfully."}, status=status.HTTP_200_OK)
                        else:
                            return Response({"message" : "Your account has been blocked", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({"message" : "Email or Password incorrect", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : "Email or Password incorrect", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    