from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User,Group,Permission,ContentType
from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from .models import *
from auditlog.models import LogEntry

User = get_user_model()


#this is a class used to customize the JWT token obtaining since we need to send the permission list to the user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
        # Add custom claims
        #token['username'] = user.username
        token['email'] = user.email
        #token['first_name'] = user.first_name
        #token['last_name'] = user.last_name
        token['company'] = user.company.name if user.company else None
        return token

    username_field = "email"
    
    def validate(self, attrs):
        credentials={
            "email":attrs.get("email"),
            "password":attrs.get("password")
        }
    
        data = super().validate(attrs)
        user = authenticate(email=attrs['email'],password=attrs['password'])
        if user and not user.is_active:
            raise serializers.ValidationError({"error":"user is banned from the system"})
           
    

        user = authenticate(**credentials)
        
        if user is None:
            raise serializers.ValidationError({"error":"invalid credentials"})
        
        #lets add permissions to the token payload
        #permissions = user.get_all_permissions()
        data = super().validate(attrs)
        data['permissions'] = list(user.get_all_permissions())
        data['company'] = user.company.name if user.company else None
        data['email'] = user.email
        data['groups'] = list(user.groups.values_list('name',flat=True))
        return data
    
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)
    user_permissions = serializers.SlugRelatedField(slug_field="codename",queryset=Permission.objects.all(),many=True,required=False)
    groups = serializers.SlugRelatedField(slug_field="name",queryset=Group.objects.all(),many=True,required=False)
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        if self.instance is None and "password" not in data:
            raise serializers.ValidationError({"password":"This field is required when creating a new user!"})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password",None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password",None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Ensure superusers receive all permissions."""
        representation = super().to_representation(instance)

        if instance.is_superuser:
            # Get all permission codenames for superusers
            all_permissions = Permission.objects.values_list("codename", flat=True)
            representation["user_permissions"] = list(all_permissions)
        else:
            # Regular users: only show explicitly assigned permissions
            representation["user_permissions"] = list(instance.user_permissions.values_list("codename", flat=True))

        return representation
    
    def get_profile_picture(self,obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        elif obj.profile_picture:
            # fallback if no request is available
            from django.conf import settings
            return settings.SITE_URL + obj.profile_picture.url
        return None
    
class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(slug_field="codename",queryset=Permission.objects.all(),many=True,required=False)

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(write_only=True,queryset=ContentType.objects.all())
    class Meta:
        model = Permission
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = "__all__"

class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = "__all__"

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"

class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = "__all__"

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = "__all__"

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"

class TrainingAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingAttendance
        fields = "__all__"

class EmployeeGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGoal
        fields = "__all__"

class PayrollCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollCalendar
        fields = "__all__"

class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = "__all__"

class OvertimePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimePolicy
        fields = "__all__"

class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = "__all__"


class PayrollAdditionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollAdditionType
        fields = "__all__"

class PayrollAdditionSerializer(serializers.ModelSerializer):
    addition_type = serializers.SlugRelatedField(slug_field="name", queryset=PayrollAdditionType.objects.all())

    class Meta:
        model = PayrollAddition
        fields = "__all__"

class PayrollDeductionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeductionType
        fields = "__all__"

class PayrollDeductionSerializer(serializers.ModelSerializer):
    deduction_type = serializers.SlugRelatedField(slug_field="name", queryset=PayrollDeductionType.objects.all())

    class Meta:
        model = PayrollDeduction
        fields = "__all__"

class PensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pension
        fields = "__all__"

class PayrollPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPolicy
        fields = "__all__"    

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"

class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        fields = "__all__"   