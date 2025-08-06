from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import SubscriptionPlanService
from ..serializers import SubscriptionPlanServiceSerializer
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

class SubscriptionPlanServiceListView(generics.ListAPIView):
    """
    API endpoint that allows SubscriptionPlanService to be viewed.
    """
    queryset = SubscriptionPlanService.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in SubscriptionPlanService._meta.fields]
    ordering_fields = [field.name for field in SubscriptionPlanService._meta.fields]
    pagination_class = CustomPagination
    serializer_class = SubscriptionPlanServiceSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'is_active': ['exact'],
    'subscription_plan__name':['exact'],
    'company__name': ['exact','icontains'],
    }

class SubscriptionPlanServiceRetrieveView(generics.RetrieveAPIView):
    queryset = SubscriptionPlanService.objects.all()
    serializer_class = SubscriptionPlanServiceSerializer
    permission_classes = []
    lookup_field = ['id']

class SubscriptionPlanServiceUpdateView(generics.UpdateAPIView):
    queryset = SubscriptionPlanService.objects.all()
    serializer_class = SubscriptionPlanServiceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class SubscriptionPlanServiceDestroyView(generics.DestroyAPIView):
    queryset = SubscriptionPlanService.objects.all()
    serializer_class = SubscriptionPlanServiceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class SubscriptionPlanServiceCreateView(generics.CreateAPIView):
    queryset = SubscriptionPlanService.objects.all()
    serializer_class = SubscriptionPlanServiceSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  