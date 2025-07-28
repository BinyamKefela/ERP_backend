from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import PerformanceReview
from ..serializers import PerformanceReviewSerializer
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


class PerformanceReviewListView(generics.ListAPIView):
    """
    API endpoint that allows companies to be viewed.
    """
    queryset = PerformanceReview.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in PerformanceReview._meta.fields]
    ordering_fields = [field.name for field in PerformanceReview._meta.fields]
    pagination_class = CustomPagination
    serializer_class = PerformanceReviewSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'employee__user__email':['exact','icontains'],
    'reviewer__user__email': ['exact','icontains'],
    'company__name': ['exact','icontains']  ,
     }
    

    def get_queryset(self):
        queryset = super().get_queryset()
        min_review_date = self.request.GET.get('min_review_date')
        max_review_date = self.request.GET.get('max_review_date')
        min_review_period_start = self.request.GET.get('min_review_period_start')
        max_review_period_start = self.request.GET.get('max_review_period_start')
        min_review_period_end = self.request.GET.get('min_review_period_end')
        max_review_period_end = self.request.GET.get('max_review_period_end')

        if min_review_date:
            try:
                min_review_date = datetime.datetime.strptime(min_review_date, '%Y-%m-%d').date()
                queryset = queryset.filter(review_date__gte=min_review_date)
            except ValueError:
                raise NotFound("Invalid min_review_date format. Use YYYY-MM-DD.")
        if max_review_date:
            try:
                max_review_date = datetime.datetime.strptime(max_review_date, '%Y-%m-%d').date()
                queryset = queryset.filter(review_date__lte=max_review_date)
            except ValueError:
                raise NotFound("Invalid max_review_date format. Use YYYY-MM-DD.")
        if min_review_period_start:
            try:
                min_review_period_start = datetime.datetime.strptime(min_review_period_start, '%Y-%m-%d').date()
                queryset = queryset.filter(review_period_start__gte=min_review_period_start)
            except ValueError:
                raise NotFound("Invalid min_review_period_start format. Use YYYY-MM-DD.")
        if max_review_period_start:
            try:
                max_review_period_start = datetime.datetime.strptime(max_review_period_start, '%Y-%m-%d').date()
                queryset = queryset.filter(review_period_start__lte=max_review_period_start)
            except ValueError:
                raise NotFound("Invalid max_review_period_start format. Use YYYY-MM-DD.")
        if min_review_period_end:
            try:
                min_review_period_end = datetime.datetime.strptime(min_review_period_end, '%Y-%m-%d').date()
                queryset = queryset.filter(review_period_end__gte=min_review_period_end)
            except ValueError:
                raise NotFound("Invalid min_review_period_end format. Use YYYY-MM-DD.")
        if max_review_period_end:
            try:
                max_review_period_end = datetime.datetime.strptime(max_review_period_end, '%Y-%m-%d').date()
                queryset = queryset.filter(review_period_end__lte=max_review_period_end)
            except ValueError:
                raise NotFound("Invalid max_review_period_end format. Use YYYY-MM-DD.")
        return queryset

class PerformanceReviewRetrieveView(generics.RetrieveAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class PerformanceReviewUpdateView(generics.UpdateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class PerformanceReviewDestroyView(generics.DestroyAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class PerformanceReviewCreateView(generics.CreateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


    