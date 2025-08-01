from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PayrollDeduction
from ..serializers import PayrollDeductionSerializer
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

class PayrollDeductionListView(generics.ListAPIView):
    """
    API endpoint that allows PayrollDeduction to be viewed.
    """
    queryset = PayrollDeduction.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PayrollDeduction._meta.fields]
    ordering_fields = [field.name for field in PayrollDeduction._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PayrollDeductionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'company_name': ['exact','icontains'],
    }

class PayrollDeductionRetrieveView(generics.RetrieveAPIView):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PayrollDeductionUpdateView(generics.UpdateAPIView):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PayrollDeductionDestroyView(generics.DestroyAPIView):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PayrollDeductionCreateView(generics.CreateAPIView):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  