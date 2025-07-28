from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import WorkHistory
from ..serializers import WorkHistorySerializer
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


class WorkHistoryListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = WorkHistory.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in WorkHistory._meta.fields]
    ordering_fields = [field.name for field in WorkHistory._meta.fields]
    pagination_class = CustomPagination
    serializer_class = WorkHistorySerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'position__title':['exact','icontains'],
    'employee__user__email': ['exact','icontains'],
    'company__name': ['exact','icontains'],
     }

class WorkHistoryRetrieveView(generics.RetrieveAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class WorkHistoryUpdateView(generics.UpdateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class WorkHistoryDestroyView(generics.DestroyAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class WorkHistoryCreateView(generics.CreateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


   