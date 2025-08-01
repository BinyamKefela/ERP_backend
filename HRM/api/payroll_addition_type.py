from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PayrollAdditionType
from ..serializers import PayrollAdditionTypeSerializer
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


load_dotenv()

class PayrollAdditionTypeListView(generics.ListAPIView):
    """
    API endpoint that allows PayrollAdditionType to be viewed.
    """
    queryset = PayrollAdditionType.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PayrollAdditionType._meta.fields]
    ordering_fields = [field.name for field in PayrollAdditionType._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PayrollAdditionTypeSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'company_name': ['exact','icontains'],
    'name': ['exact', 'icontains'],
    'is_active': ['exact'],
    }

class PayrollAdditionTypeRetrieveView(generics.RetrieveAPIView):
    queryset = PayrollAdditionType.objects.all()
    serializer_class = PayrollAdditionTypeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PayrollAdditionTypeUpdateView(generics.UpdateAPIView):
    queryset = PayrollAdditionType.objects.all()
    serializer_class = PayrollAdditionTypeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PayrollAdditionTypeDestroyView(generics.DestroyAPIView):
    queryset = PayrollAdditionType.objects.all()
    serializer_class = PayrollAdditionTypeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PayrollAdditionTypeCreateView(generics.CreateAPIView):
    queryset = PayrollAdditionType.objects.all()
    serializer_class = PayrollAdditionTypeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  