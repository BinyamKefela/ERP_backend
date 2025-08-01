from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Transfer
from ..serializers import TransferSerializer
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

class TransferListView(generics.ListAPIView):
    """
    API endpoint that allows Transfer to be viewed.
    """
    queryset = Transfer.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Transfer._meta.fields]
    ordering_fields = [field.name for field in Transfer._meta.fields]
    pagination_class = CustomPagination
    serializer_class = TransferSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'employee__email':['exact','icontains'],
    'from_branch__name': ['exact', 'icontains'],
    'to_branch__name': ['exact', 'icontains'],
    'status': ['exact', 'icontains'],
    'transfer_date': ['exact', 'gte', 'lte'],
    'created_at': ['exact', 'gte', 'lte'],
    'company_name': ['exact','icontains'],
    }

class TransferRetrieveView(generics.RetrieveAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class TransferUpdateView(generics.UpdateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class TransferDestroyView(generics.DestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class TransferCreateView(generics.CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  