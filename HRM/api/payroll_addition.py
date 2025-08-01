from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PayrollAddition
from ..serializers import PayrollAdditionSerializer
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

class PayrollAdditionListView(generics.ListAPIView):
    """
    API endpoint that allows PayrollAddition to be viewed.
    """
    queryset = PayrollAddition.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PayrollAddition._meta.fields]
    ordering_fields = [field.name for field in PayrollAddition._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PayrollAdditionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'payroll_employee__email':['exact','icontains'],
    'company_name': ['exact','icontains'],
    }

class PayrollAdditionRetrieveView(generics.RetrieveAPIView):
    queryset = PayrollAddition.objects.all()
    serializer_class = PayrollAdditionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PayrollAdditionUpdateView(generics.UpdateAPIView):
    queryset = PayrollAddition.objects.all()
    serializer_class = PayrollAdditionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PayrollAdditionDestroyView(generics.DestroyAPIView):
    queryset = PayrollAddition.objects.all()
    serializer_class = PayrollAdditionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PayrollAdditionCreateView(generics.CreateAPIView):
    queryset = PayrollAddition.objects.all()
    serializer_class = PayrollAdditionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  