from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Attendance
from ..serializers import AttendanceSerializer
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


class AttendanceListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Attendance._meta.fields]
    ordering_fields = [field.name for field in Attendance._meta.fields]
    pagination_class = CustomPagination
    serializer_class = AttendanceSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'employee__user__email':['exact','icontains'],
    'date': ['exact','icontains'],
    'company__name': ['exact','icontains'],
     }
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_date = self.request.GET.get('min_date')
        max_date = self.request.GET.get('max_date')

        if min_date:
            try:
                min_date = datetime.datetime.strptime(min_date,'%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=min_date)
            except ValueError:
                raise NotFound("Invalid min_date format. Use YYYY-MM-DD.")
        if max_date:
            try:
                max_date = datetime.datetime.strptime(max_date,'%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=max_date)
            except ValueError:
                raise NotFound("Invalid max_date format. Use YYYY-MM-DD.")
        return queryset

class AttendanceRetrieveView(generics.RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class AttendanceUpdateView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class AttendanceDestroyView(generics.DestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


 