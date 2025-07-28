from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import TrainingAttendance
from ..serializers import TrainingAttendanceSerializer
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


class TrainingAttendanceListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = TrainingAttendance.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in TrainingAttendance._meta.fields]
    ordering_fields = [field.name for field in TrainingAttendance._meta.fields]
    pagination_class = CustomPagination
    serializer_class = TrainingAttendanceSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'training__name':['exact','icontains'],
    'employee__user__email':['exact'],
    'company__name': ['exact','icontains']  ,
     }
    

    def get_queryset(self):
        queryset = super().get_queryset()
        min_start_date = self.request.GET.get('min_start_date')
        max_start_date = self.request.GET.get('max_start_date')

        if min_start_date:
            try:
                min_start_date = datetime.datetime.strptime(min_start_date,'%Y-%m-%d').date()
                queryset = queryset.filter(start_date__gte=min_start_date)
            except ValueError:
                raise NotFound("Invalid min_start_date format. Use YYYY-MM-DD.")
            
        if max_start_date:
            try:
                max_start_date = datetime.datetime.strptime(max_start_date,'%Y-%m-%d').date()
                queryset = queryset.filter(start_date__lte=max_start_date)
            except ValueError:
                raise NotFound("Invalid max_start_date format. Use YYYY-MM-DD.")
            
        return queryset

class TrainingAttendanceRetrieveView(generics.RetrieveAPIView):
    queryset = TrainingAttendance.objects.all()
    serializer_class = TrainingAttendanceSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class TrainingAttendanceUpdateView(generics.UpdateAPIView):
    queryset = TrainingAttendance.objects.all()
    serializer_class = TrainingAttendanceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class TrainingAttendanceDestroyView(generics.DestroyAPIView):
    queryset = TrainingAttendance.objects.all()
    serializer_class = TrainingAttendanceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class TrainingAttendanceCreateView(generics.CreateAPIView):
    queryset = TrainingAttendance.objects.all()
    serializer_class = TrainingAttendanceSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    