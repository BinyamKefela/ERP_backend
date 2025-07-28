from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PayrollPeriod
from ..serializers import PayrollPeriodSerializer
from HRM.api.custom_pagination import CustomPagination
import datetime
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view,permission_classes
from dotenv import load_dotenv
from django.contrib.auth import get_user_model

User = get_user_model()


class PayrollPeriodListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = PayrollPeriod.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PayrollPeriod._meta.fields]
    ordering_fields = [field.name for field in PayrollPeriod._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PayrollPeriodSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'company__name': ['exact','icontains']  ,
     }
    

class PayrollPeriodRetrieveView(generics.RetrieveAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PayrollPeriodUpdateView(generics.UpdateAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PayrollPeriodDestroyView(generics.DestroyAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PayrollPeriodCreateView(generics.CreateAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    