from django.db import models

from django.contrib.auth.models import  AbstractUser,AbstractBaseUser,BaseUserManager,PermissionsMixin,Group
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from datetime import timedelta

import uuid
from auditlog.registry import auditlog

# Create your models here.


def validate_uploaded_image_extension(value):
    valid_extensions = ['.png','.jpg','.jpeg','.PNG','.JPG','.JPEG']
    ext = os.path.splitext(value.name)[1]
    if not ext in valid_extensions:
        raise ValidationError('Unsupported filed extension')
        

def get_upload_path(instance,filename):
    ext = filename.split('.')[-1]
    new_file_name = "profiles/"+f'{instance.id}.{ext}'
    return new_file_name

# Custom manager for user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='company_owner')
    calendar_type = models.CharField(
        max_length=10, 
        choices=[('GREGORIAN', 'Gregorian'), ('ETHIOPIAN', 'Ethiopian')],
        default='GREGORIAN'
    )
    base_currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    company_type = models.CharField(choices=[('private', 'private'), ('public', 'public'),('military and public','military and public')], max_length=10, default='Private')
    
    
    def __str__(self):
        return self.name
    

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,null=True)
    middle_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    profile_picture = models.FileField(upload_to=get_upload_path,validators=[validate_uploaded_image_extension],null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    is_company_admin = models.BooleanField(default=False)

    # Make groups and user_permissions optional by adding blank=True and null=True
    groups = models.ManyToManyField(
        'auth.Group', 
        blank=True,
        null=True, 
        related_name='customuser_set', 
        related_query_name='customuser', 
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        blank=True,
        null=True, 
        related_name='customuser_set', 
        related_query_name='customuser', 
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # fields to be used when creating a superuser
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        return super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        return super().save(*args, **kwargs)


auditlog.register(User)


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.user.email}"

class EmailResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)


    
GENDER_CHOICES = [('M','Male'),('F','Female')]
MARITAL_STATUS = [('S','Single'),('M','Married'),('D','Divorced'),('W','Widowed')]
EMPLOYMENT_TYPE = [('FT','Full Time'),('PT','Part Time'),('CT','Contract'),('IN','Internship')]

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    employee_id = models.CharField(max_length=100,unique=True,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=100,choices=MARITAL_STATUS)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    postal_code = models.CharField(max_length=100,null=True,blank=True)
    hire_date = models.DateField()
    employment_type = models.CharField(max_length=100,choices=EMPLOYMENT_TYPE)
    status = models.CharField(max_length=100,choices=[('A','Active'),('I','Inactive')],default='A')
    profile_picture = models.FileField(upload_to=get_upload_path,validators=[validate_uploaded_image_extension],null=True,blank=True)


    emergency_contact_name = models.CharField(max_length=100,null=True,blank=True)
    emergency_contact_phone = models.CharField(max_length=100,null=True,blank=True)
    emergency_contact_relationship = models.CharField(max_length=100,null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.employee_id})'


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Position(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.department.name})"
    
class Employment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='employment')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    salary_currency = models.CharField(max_length=3, default='USD')
    #payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE)
    bank_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee} - {self.position}"
    
class WorkHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Work Histories"
        #ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.employee}: {self.position} ({self.start_date} - {self.end_date or 'Present'})"
    


ATTENDANCE_STATUS_CHOICES = [
    ('Present', 'Present'),('Absent', 'Absent'),
    ('Late', 'Late'),('On Leave', 'On Leave'),]


class Attendance(models.Model):
    OVERTIME_TYPE_CHOICES = [
        ('WEEKDAY', 'Weekday'),
        ('WEEKEND', 'Weekend'),
        ('HOLIDAY', 'Holiday'),
        ('NIGHT', 'Night Shift'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default='Present')
    notes = models.TextField(blank=True)

    # Overtime fields
    regular_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_type = models.CharField(max_length=20, choices=OVERTIME_TYPE_CHOICES, blank=True)
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    overtime_approved = models.BooleanField(default=False)
    overtime_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, 
                                           null=True, blank=True, related_name='approved_overtimes')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('employee', 'date')
        #ordering = ['-date', 'employee']
    
    def __str__(self):
        return f"{self.employee} - {self.date}: {self.status}"
    

LEAVE_TYPE_CHOICES = [
    ('Sick Leave', 'Sick Leave'),('Casual Leave', 'Casual Leave'),
    ('Annual Leave', 'Annual Leave'),('Maternity Leave', 'Maternity Leave'),]

LEAVE_STATUS_CHOICES = [
    ('Pending', 'Pending'),('Approved', 'Approved'),('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled'),]

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    date_applied = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.employee}: {self.leave_type} ({self.start_date} to {self.end_date})"

JOB_OPENING_STATUS_CHOICES = [
    ('Open', 'Open'),('Closed', 'Closed'),]   

class JobOpening(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    opening_date = models.DateField()
    closing_date = models.DateField(null=True, blank=True)
    expected_hire_date = models.DateField(null=True, blank=True)
    number_of_openings = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=JOB_OPENING_STATUS_CHOICES, default='Open')
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.position} - {self.status}"
    

APPLICANT_STATUS_CHOICES = [
    ('Applied', 'Applied'),('Interviewed', 'Interviewed'),('Offered', 'Offered'),
    ('Hired', 'Hired'),('Rejected', 'Rejected'),]



class Applicant(models.Model):
    first_name = models.CharField(max_length=50)
    mddle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='applicants/resumes/')
    cover_letter = models.FileField(upload_to='applicants/cover_letters/', null=True, blank=True)
    applied_for = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS_CHOICES, default='Applied')
    notes = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applied_for.position}"
    

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews_given')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    review_date = models.DateField()
    max_rating_point = models.DecimalField(max_digits=3,decimal_places=1,null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1,null=True, blank=True)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    comments = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    next_review_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
    def __str__(self):
        return f"Performance Review for {self.employee} on {self.review_date}"
    

GOAL_STATUS_CHOICES = [
    ('Not Started', 'Not Started'),('In Progress', 'In Progress'),('Completed', 'Completed'),
    ('On Hold', 'On Hold'),('Cancelled', 'Cancelled'),]
class Goal(models.Model):
    #employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=GOAL_STATUS_CHOICES, default='Not Started')
    progress = models.PositiveIntegerField(default=0)
    key_result = models.TextField()
    #review = models.ForeignKey(PerformanceReview, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee}: {self.title}"

class EmployeeGoal(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal,on_delete=models.CASCADE)
    max_rating_point = models.DecimalField(max_digits=3,decimal_places=1,null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1,null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)


 
    

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='general_documents/')
    document_type = models.CharField(max_length=50)
    #issue_date = models.DateField(null=True, blank=True)
    #expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.employee}: {self.name}"
    

class Training(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    max_participants = models.PositiveIntegerField()
    participants = models.ManyToManyField(Employee, through='TrainingAttendance')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class TrainingAttendance(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    max_score = models.DecimalField(max_digits=3,decimal_places=1,null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('training', 'employee')
    
    def __str__(self):
        return f"{self.employee} - {self.training}"


class PayrollCalendar(models.Model):
    CALENDAR_CHOICES = [
        ('GREGORIAN', 'Gregorian'),
        ('ETHIOPIAN', 'Ethiopian'),
    ]
    
    name = models.CharField(max_length=100)
    calendar_type = models.CharField(max_length=10, choices=CALENDAR_CHOICES, default='GREGORIAN')
    start_day = models.PositiveIntegerField(help_text="Day of month when payroll period starts")
    payment_day = models.PositiveIntegerField(help_text="Day of month when payment is made")
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.calendar_type})"
    

class PayrollPeriod(models.Model):
    calendar = models.ForeignKey(PayrollCalendar, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField()
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        unique_together = ('calendar', 'start_date', 'end_date')
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"


class Payroll(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Transfer'),
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('MOBILE', 'Mobile Money'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    period = models.ForeignKey(PayrollPeriod, on_delete=models.PROTECT)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_additions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('employee', 'period')
        ordering = ['period', 'employee']
    
    def __str__(self):
        return f"{self.employee} - {self.period} - {self.net_salary}"
    


class PayrollAdditionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    is_taxable = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class PayrollDeductionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    is_tax_exempt = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class PayrollAddition(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='additions')
    addition_type = models.ForeignKey(PayrollAdditionType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.payroll}: {self.addition_type} - {self.amount}"

class PayrollDeduction(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions')
    deduction_type = models.ForeignKey(PayrollDeductionType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.payroll}: {self.deduction_type} - {self.amount}"
    

class OvertimePolicy(models.Model):
    OVERTIME_TYPE_CHOICES = [
        ('WEEKDAY', 'Weekday'),
        ('WEEKEND', 'Weekend'),
        ('HOLIDAY', 'Holiday'),
        ('NIGHT', 'Night Shift'),
    ]
    
    name = models.CharField(max_length=100)
    overtime_type = models.CharField(max_length=10, choices=OVERTIME_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Multiplier of base salary")
    minimum_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Overtime Policies"
        unique_together = ('overtime_type', 'effective_date')
    
    def __str__(self):
        return f"{self.name} ({self.overtime_type} - {self.rate}x)"
    

class TaxRate(models.Model):
    minimum_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maximum_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage rate")
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Tax Rates"
        unique_together = ('minimum_income', 'maximum_income')
    
    def __str__(self):
        return f"Tax rate - {self.rate}%"
    

class Deduction(models.Model):
    minimum_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maximum_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage rate")
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Tax Rates"
        unique_together = ('minimum_income', 'maximum_income')
    
    def __str__(self):
        return f"Deduction - {self.deduction}%"


class Pension(models.Model):
    PENSION_TYPES = [('private','private'),('public','public'),('military and police','military and police')]
    pension_type = models.CharField(choices=PENSION_TYPES)
    employee_pension = models.FloatField()
    company_pension = models.FloatField()


class PayrollPolicy(models.Model):
    WORKING_DAYS_POLICY_CHOICES = ['fixed 30 days','monthly days']
    working_days_policy = models.CharField(max_length=100,choices=WORKING_DAYS_POLICY_CHOICES)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)