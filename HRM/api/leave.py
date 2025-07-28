from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Leave
from ..serializers import LeaveSerializer
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


class LeaveListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = Leave.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Leave._meta.fields]
    ordering_fields = [field.name for field in Leave._meta.fields]
    pagination_class = CustomPagination
    serializer_class = LeaveSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'emoloyee__user__email':['exact','icontains'],
    'leave_type': ['exact','icontains'],
    'company__name': ['exact','icontains'],
     }
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_start_date = self.request.GET.get('min_start_date')
        max_start_date = self.request.GET.get('max_start_date')
        min_end_date = self.request.GET.get('min_end_date')
        max_end_date = self.request.GET.GET('max_start_date')
        min_date_applied = self.request.GET.get('min_date_applied')
        max_date_applied = self.request.GET.get('max_date_applied')

        if min_start_date:
            try:
                min_start_date = datetime.datetime.strptime(min_start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__gte=min_start_date)
            except ValueError:
                raise NotFound("Invalid min_start_date format. Use YYYY-MM-DD.")
        if max_start_date:
            try:
                max_start_date = datetime.datetime.strptime(max_start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__lte=max_start_date)
            except ValueError:
                raise NotFound("Invalid max_start_date format. Use YYYY-MM-DD.")
        if min_end_date:
            try:
                min_end_date = datetime.datetime.strptime(min_end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(end_date__gte=min_end_date)
            except ValueError:
                raise NotFound("Invalid min_end_date format. Use YYYY-MM-DD.")
        if max_end_date:
            try:
                max_end_date = datetime.datetime.strptime(max_end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(end_date__lte=max_end_date)
            except ValueError:
                raise NotFound("Invalid max_end_date format. Use YYYY-MM-DD.")
        if min_date_applied:
            try:
                min_date_applied = datetime.datetime.strptime(min_date_applied, '%Y-%m-%d').date()
                queryset = queryset.filter(date_applied__gte=min_date_applied)
            except ValueError:
                raise NotFound("Invalid min_date_applied format. Use YYYY-MM-DD.")
        if max_date_applied:
            try:
                max_date_applied = datetime.datetime.strptime(max_date_applied, '%Y-%m-%d').date()
                queryset = queryset.filter(date_applied__lte=max_date_applied)
            except ValueError:
                raise NotFound("Invalid max_date_applied format. Use YYYY-MM-DD.")
        return queryset
        

      

class LeaveRetrieveView(generics.RetrieveAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class LeaveUpdateView(generics.UpdateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class LeaveDestroyView(generics.DestroyAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class LeaveCreateView(generics.CreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


