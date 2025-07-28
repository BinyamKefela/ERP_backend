from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import JobOpening
from ..serializers import JobOpeningSerializer
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


class JobOpeningListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = JobOpening.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in JobOpening._meta.fields]
    ordering_fields = [field.name for field in JobOpening._meta.fields]
    pagination_class = CustomPagination
    serializer_class = JobOpeningSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'position__title':['exact','icontains'],
    'position__department__name': ['exact','icontains'],
    'salary_range': ['exact','icontains'],
    'status': ['exact','icontains'],
    'company__name': ['exact','icontains']  ,
     }
    

    def get_queryset(self):
        queryset = super().get_queryset()
        min_opening_date = self.request.query_params.get('min_opening_date')
        max_opening_date = self.request.query_params.get('max_opening_date')
        min_closing_date = self.request.query_params.get('min_closing_date')
        max_closing_date = self.request.query_params.get('max_closing_date')
        if min_opening_date:
            try:
                min_opening_date = datetime.datetime.strptime(min_opening_date, '%Y-%m-%d').date()
                queryset = queryset.filter(opening_date__gte=min_opening_date)
            except ValueError:
                raise NotFound("Invalid min_opening_date format. Use YYYY-MM-DD.")
        if max_opening_date:
            try:
                max_opening_date = datetime.datetime.strptime(max_opening_date, '%Y-%m-%d').date()
                queryset = queryset.filter(opening_date__lte=max_opening_date)
            except ValueError:
                raise NotFound("Invalid max_opening_date format. Use YYYY-MM-DD.")
        if min_closing_date:
            try:
                min_closing_date = datetime.datetime.strptime(min_closing_date, '%Y-%m-%d').date()
                queryset = queryset.filter(closing_date__gte=min_closing_date)
            except ValueError:
                raise NotFound("Invalid min_closing_date format. Use YYYY-MM-DD.")
        if max_closing_date:
            try:
                max_closing_date = datetime.datetime.strptime(max_closing_date, '%Y-%m-%d').date()
                queryset = queryset.filter(closing_date__lte=max_closing_date)
            except ValueError:
                raise NotFound("Invalid max_closing_date format. Use YYYY-MM-DD.")
        return queryset

class JobOpeningRetrieveView(generics.RetrieveAPIView):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class JobOpeningUpdateView(generics.UpdateAPIView):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class JobOpeningDestroyView(generics.DestroyAPIView):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class JobOpeningCreateView(generics.CreateAPIView):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    