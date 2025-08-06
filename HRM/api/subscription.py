from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Subscription
from ..serializers import SubscriptionSerializer
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

class SubscriptionListView(generics.ListAPIView):
    """
    API endpoint that allows Subscription to be viewed.
    """
    queryset = Subscription.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Subscription._meta.fields]
    ordering_fields = [field.name for field in Subscription._meta.fields]
    pagination_class = CustomPagination
    serializer_class = SubscriptionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'is_active': ['exact'],
    #'subscription_plan__name':['exact'],
    'company__name': ['exact','icontains'],
    }

class SubscriptionRetrieveView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = []
    lookup_field = ['id']

class SubscriptionUpdateView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class SubscriptionDestroyView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  