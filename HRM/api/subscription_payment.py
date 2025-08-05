from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import SubscriptionPayment
from ..serializers import SubscriptionPaymentSerializer
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

class SubscriptionPaymentListView(generics.ListAPIView):
    """
    API endpoint that allows SubscriptionPayment to be viewed.
    """
    queryset = SubscriptionPayment.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in SubscriptionPayment._meta.fields]
    ordering_fields = [field.name for field in SubscriptionPayment._meta.fields]
    pagination_class = CustomPagination
    serializer_class = SubscriptionPaymentSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'transaction_id':['exact','icontains'],
    'payment_date': ['exact', 'year__gt', 'year__lt', 'month__gt', 'month__lt'],
    'is_successful': ['exact', 'icontains'],
    'subscription__company__name': ['exact','icontains'],
    }

class SubscriptionPaymentRetrieveView(generics.RetrieveAPIView):
    queryset = SubscriptionPayment.objects.all()
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class SubscriptionPaymentUpdateView(generics.UpdateAPIView):
    queryset = SubscriptionPayment.objects.all()
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class SubscriptionPaymentDestroyView(generics.DestroyAPIView):
    queryset = SubscriptionPayment.objects.all()
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class SubscriptionPaymentCreateView(generics.CreateAPIView):
    queryset = SubscriptionPayment.objects.all()
    serializer_class = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  