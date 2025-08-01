from ..models import *
from rest_framework.decorators import api_view
from dotenv import load_dotenv
import os
from django.db.models import Sum
from ethiopian_date_converter.ethiopian_date_convertor import to_ethiopian,to_gregorian
from rest_framework.response import Response
import rest_framework.status as status


load_dotenv()


ETHIOPIAN_MONTHS = ['MESKEREM','TIQIMT','HIDAR','TAHSASE','TIR','YEKATIT','MEGABIT','MIAZIA','GENBOT','SENE','HAMLE','NEHASSE','PAGUMEN']


# a method to get the overall net salary of an employee
def calculate_total_net_salary(gross_salary,company):
    tax_rate = float(TaxRate.objects.filter(is_active=True,minimum_income__gte=gross_salary,maximum_income__lte=gross_salary).first().rate)
    deduction = float(Deduction.objects.filter(is_active=True,minimum_income__gte=gross_salary,maximum_income__lte=gross_salary).first().deduction)
    employment_income_tax = (gross_salary*tax_rate-deduction)
    pension = gross_salary*Pension.objects.filter(pension_type=company.company_type).first().employee_pension/100

    total_deduction = PayrollDeduction.objects.aggregate(total_deduction=Sum('amount'))['total_deduction'] or 0
    net_salary = gross_salary-employment_income_tax-total_deduction-float(pension)

    return net_salary


# a method to get the total working days of an employee in a given payroll period
def get_total_working_days(employee_id,payroll_period_id,company_id):
    calendar = PayrollCalendar.objects.filter(is_active=True).first()
    payroll_period = PayrollPeriod.objects.filter(id=payroll_period_id).first()
    employee = Employee.objects.filter(id=employee_id).first()
    company = Company.objects.filter(id=company_id).first()
    start_date = payroll_period.start_date
    end_date = payroll_period.end_date
    if calendar.calendar_type == PayrollCalendar.CALENDAR_CHOICES[1]:
        start_date = to_gregorian(payroll_period.start_date)
        end_date = to_gregorian(payroll_period.end_date)
    absent_working_days = Attendance.objects.filter(employee=employee,date__gte=start_date,
                                                date__lte=end_date,status='Absent',company=company).count()
    
    working_days_policy = PayrollPolicy.objects.filter(company=company,is_active=True).first()

    if working_days_policy.working_days_policy == PayrollPolicy.WORKING_DAYS_POLICY_CHOICES[1]:
        return 30-int(absent_working_days)
    else:
        import calendar
        from datetime import datetime
        return calendar.monthrange(datetime.date(end_date).year,datetime.strptime(end_date).month)-int(absent_working_days)


# a method to get the salary of an employee in a given payroll period after calculating the days he was present
def calculate_net_salary(employee,payroll_period):
    calendar = PayrollCalendar.objects.filter(is_active=True).first()
    start_date = payroll_period.start_date
    end_date = payroll_period.end_date
    #payroll_period = PayrollPeriod.objects.filter(id=payroll_period_id).first()
    working_days_policy = PayrollPolicy.objects.filter(company=employee.company,is_active=True).first()
    if working_days_policy.working_days_policy == PayrollPolicy.WORKING_DAYS_POLICY_CHOICES[1]:
        return calculate_total_net_salary(employee.gross_salary,employee.company)/30*get_total_working_days(employee.id,payroll_period.id,employee.company.id) 
    else:
        import calendar
        from datetime import datetime
        return calculate_total_net_salary(employee.gross_salary,employee.company)/calendar.monthrange(datetime.date(end_date).year,datetime.strptime(end_date).month)*get_total_working_days(employee.id,payroll_period.id,employee.company.id) 



@api_view(['GET'])
def get_payroll(request,payroll_period):
    payroll_period = PayrollPeriod.objects.filter(id=payroll_period).first()
    employees = Employee.objects.filter(status='ACTIVE')
    employee_list = []

    for employee in employees:
        employee_list.append({'employee':employee,'net_salary':calculate_net_salary(employee=employee,payroll_period=payroll_period),})
    return Response({'data':employee_list},status=status.HTTP_200_OK)

