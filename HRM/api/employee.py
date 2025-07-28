from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Employee
from ..serializers import EmployeeSerializer
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


class EmployeeListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Employee._meta.fields]
    ordering_fields = [field.name for field in Employee._meta.fields]
    pagination_class = CustomPagination
    serializer_class = EmployeeSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact','icontains'],
    'owner__email': ['exact','icontains'],
    'company__name': ['exact','icontains'],
     }

class EmployeeRetrieveView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class EmployeeDestroyView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    def perform_create(self, serializer):
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        first_name = serializer.validated_data.get('first_name')
        middle_name = serializer.validated_data.get('middle_name')
        last_name = serializer.validated_data.get('last_name')

        user = User()
        user.email= email
        user.first_name = first_name
        middle_name = middle_name
        last_name = last_name
        user.save()

        serializer.save()
        recepient_email_address = user.email
        message = f"Dear {user.first_name},\n your user account has been created successfully. please contact the admin for credentials.\n" 
        subject = "Account Creation Notification"       
        load_dotenv()
        import os
        from_email = os.getenv('EMAIL_HOST_USER')

        from django.core.mail import send_mail
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recepient_email_address],
            fail_silently=False
        )