from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from apis.models import Item, User
from apis.serializers import ItemSerializer, UserSerializer
from apis.decorators import login_required
from django.utils.decorators import method_decorator

#@method_decorator(login_required, name='dispatch')
class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

#@method_decorator(login_required, name='dispatch')
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
