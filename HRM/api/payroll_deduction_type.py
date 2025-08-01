from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PayrollDeductionType
from ..serializers import PayrollDeductionTypeSerializer
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

class PayrollDeductionTypeListView(generics.ListAPIView):
    """
    API endpoint that allows PayrollDeductionType to be viewed.
    """
    queryset = PayrollDeductionType.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PayrollDeductionType._meta.fields]
    ordering_fields = [field.name for field in PayrollDeductionType._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PayrollDeductionTypeSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'company_name': ['exact','icontains'],
    }

class PayrollDeductionTypeRetrieveView(generics.RetrieveAPIView):
    queryset = PayrollDeductionType.objects.all()
    serializer_class = PayrollDeductionTypeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PayrollDeductionTypeUpdateView(generics.UpdateAPIView):
    queryset = PayrollDeductionType.objects.all()
    serializer_class = PayrollDeductionTypeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PayrollDeductionTypeDestroyView(generics.DestroyAPIView):
    queryset = PayrollDeductionType.objects.all()
    serializer_class = PayrollDeductionTypeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PayrollDeductionTypeCreateView(generics.CreateAPIView):
    queryset = PayrollDeductionType.objects.all()
    serializer_class = PayrollDeductionTypeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  