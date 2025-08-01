from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Pension
from ..serializers import PensionSerializer
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

class PensionListView(generics.ListAPIView):
    """
    API endpoint that allows Pension to be viewed.
    """
    queryset = Pension.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Pension._meta.fields]
    ordering_fields = [field.name for field in Pension._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PensionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'pension_type':['exact','icontains'],
    #'company_name': ['exact','icontains'],
    }

class PensionRetrieveView(generics.RetrieveAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PensionUpdateView(generics.UpdateAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PensionDestroyView(generics.DestroyAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PensionCreateView(generics.CreateAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  