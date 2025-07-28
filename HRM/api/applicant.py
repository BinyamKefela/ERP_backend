from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Applicant
from ..serializers import ApplicantSerializer
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


class ApplicantListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = Applicant.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Applicant._meta.fields]
    ordering_fields = [field.name for field in Applicant._meta.fields]
    pagination_class = CustomPagination
    serializer_class = ApplicantSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'applied_for__position__title':['exact','icontains'],
    'applied_for__position__department__name': ['exact','icontains'],
    'status': ['exact','icontains'],
    'company__name': ['exact','icontains']  ,
     }
    

    def get_queryset(self):
        queryset = super().get_queryset()
        min_applied_date = self.request.query_params.get('min_applied_date')
        max_applied_date = self.request.query_params.get('max_applied_date')
        
        if min_applied_date:
            try:
                min_applied_date = datetime.datetime.strptime(min_applied_date, '%Y-%m-%d').date()
                queryset = queryset.filter(applied_date__gte=min_applied_date)
            except ValueError:
                raise NotFound("Invalid min_applied_date format. Use YYYY-MM-DD.")
        if max_applied_date:
            try:
                max_applied_date = datetime.datetime.strptime(max_applied_date, '%Y-%m-%d').date()
                queryset = queryset.filter(applied_date__lte=max_applied_date)
            except ValueError:
                raise NotFound("Invalid max_applied_date format. Use YYYY-MM-DD.")
        return queryset

class ApplicantRetrieveView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class ApplicantUpdateView(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class ApplicantDestroyView(generics.DestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class ApplicantCreateView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    