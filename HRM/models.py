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
    
    def __str__(self):
        return self.name
    
class Position(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_description = models.TextField()
    is_active = models.BooleanField(default=True)
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(blank=True)
    
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
    
    class Meta:
        verbose_name_plural = "Work Histories"
        #ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.employee}: {self.position} ({self.start_date} - {self.end_date or 'Present'})"
    


ATTENDANCE_STATUS_CHOICES = [
    ('Present', 'Present'),('Absent', 'Absent'),
    ('Late', 'Late'),('On Leave', 'On Leave'),]


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default='Present')
    notes = models.TextField(blank=True)
    
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
    
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applied_for.position}"
    

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews_given')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    review_date = models.DateField()
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    comments = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    next_review_date = models.DateField(null=True, blank=True)
    
    
    
    def __str__(self):
        return f"Performance Review for {self.employee} on {self.review_date}"
    

GOAL_STATUS_CHOICES = [
    ('Not Started', 'Not Started'),('In Progress', 'In Progress'),('Completed', 'Completed'),
    ('On Hold', 'On Hold'),('Cancelled', 'Cancelled'),]
class Goal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=GOAL_STATUS_CHOICES, default='Not Started')
    progress = models.PositiveIntegerField(default=0)
    key_result = models.TextField()
    review = models.ForeignKey(PerformanceReview, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee}: {self.title}"

 
    

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='general_documents/')
    document_type = models.CharField(max_length=50)
    #issue_date = models.DateField(null=True, blank=True)
    #expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
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
    
    def __str__(self):
        return self.name

class TrainingAttendance(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('training', 'employee')
    
    def __str__(self):
        return f"{self.employee} - {self.training}"