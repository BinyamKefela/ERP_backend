from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import OvertimePolicy
from ..serializers import OvertimePolicySerializer
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

class OvertimePolicyListView(generics.ListAPIView):
    """
    API endpoint that allows OvertimePolicy to be viewed.
    """
    queryset = OvertimePolicy.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in OvertimePolicy._meta.fields]
    ordering_fields = [field.name for field in OvertimePolicy._meta.fields]
    pagination_class = CustomPagination
    serializer_class = OvertimePolicySerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'company_name': ['exact','icontains'],
    }

class OvertimePolicyRetrieveView(generics.RetrieveAPIView):
    queryset = OvertimePolicy.objects.all()
    serializer_class = OvertimePolicySerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class OvertimePolicyUpdateView(generics.UpdateAPIView):
    queryset = OvertimePolicy.objects.all()
    serializer_class = OvertimePolicySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class OvertimePolicyDestroyView(generics.DestroyAPIView):
    queryset = OvertimePolicy.objects.all()
    serializer_class = OvertimePolicySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class OvertimePolicyCreateView(generics.CreateAPIView):
    queryset = OvertimePolicy.objects.all()
    serializer_class = OvertimePolicySerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  