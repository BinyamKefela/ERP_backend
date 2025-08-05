from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import SubscriptionPlan
from ..serializers import SubscriptionPlanSerializer
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

class SubscrptionPlanListView(generics.ListAPIView):
    """
    API endpoint that allows SubscrptionPlan to be viewed.
    """
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in SubscriptionPlan._meta.fields]
    ordering_fields = [field.name for field in SubscriptionPlan._meta.fields]
    pagination_class = CustomPagination
    serializer_class = SubscriptionPlanSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'is_active': ['exact'],
    #'company__name': ['exact','icontains'],
    }

class SubscrptionPlanRetrieveView(generics.RetrieveAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class SubscrptionPlanUpdateView(generics.UpdateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class SubscrptionPlanDestroyView(generics.DestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class SubscrptionPlanCreateView(generics.CreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  