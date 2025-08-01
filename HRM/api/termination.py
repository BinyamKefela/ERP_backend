from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Termination
from ..serializers import TerminationSerializer
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

class TerminationListView(generics.ListAPIView):
    """
    API endpoint that allows Termination to be viewed.
    """
    queryset = Termination.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Termination._meta.fields]
    ordering_fields = [field.name for field in Termination._meta.fields]
    pagination_class = CustomPagination
    serializer_class = TerminationSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'employee__email':['exact','icontains'],
    'termination_date': ['exact', 'year__gt', 'year__lt', 'month__gt', 'month__lt'],
    'status': ['exact', 'icontains'],
    'company_name': ['exact','icontains'],
    }

class TerminationRetrieveView(generics.RetrieveAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class TerminationUpdateView(generics.UpdateAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class TerminationDestroyView(generics.DestroyAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class TerminationCreateView(generics.CreateAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  