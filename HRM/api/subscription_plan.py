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
    permission_classes = []
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
    permission_classes = []
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription_plan(request):
    plan_name = request.data.get("name")
    description = request.data.get("description")
    max_users = request.data.get("max_users")
    duration_months = request.data.get("duration_months")

    subscription_plan = SubscriptionPlan()
    subscription_plan.name = plan_name
    subscription_plan.description = description
    subscription_plan.max_users = max_users
    subscription_plan.duration_months = duration_months
    services = request.data.get("services_included")

    subscription_plan.save()


    from ..models import SubscriptionPlanService
    for service in services:
        subscription_plan_service = SubscriptionPlanService()
        subscription_plan_service.subscription_plan = subscription_plan
        subscription_plan_service.service_name = service['service_name']
        subscription_plan_service.price = service['price']
        subscription_plan_service.is_active = False

        subscription_plan_service.save()

    return Response({"message":"successfully created plan!"},status=status.HTTP_201_CREATED)





  