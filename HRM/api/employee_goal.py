from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import EmployeeGoal
from ..serializers import EmployeeGoalSerializer
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


class EmployeeGoalListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = EmployeeGoal.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in EmployeeGoal._meta.fields]
    ordering_fields = [field.name for field in EmployeeGoal._meta.fields]
    pagination_class = CustomPagination
    serializer_class = EmployeeGoalSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'employee__user__email':['exact'],
    'company__name': ['exact','icontains']  ,
     }
    


class EmployeeGoalRetrieveView(generics.RetrieveAPIView):
    queryset = EmployeeGoal.objects.all()
    serializer_class = EmployeeGoalSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class EmployeeGoalUpdateView(generics.UpdateAPIView):
    queryset = EmployeeGoal.objects.all()
    serializer_class = EmployeeGoalSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class EmployeeGoalDestroyView(generics.DestroyAPIView):
    queryset = EmployeeGoal.objects.all()
    serializer_class = EmployeeGoalSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class EmployeeGoalCreateView(generics.CreateAPIView):
    queryset = EmployeeGoal.objects.all()
    serializer_class = EmployeeGoalSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    