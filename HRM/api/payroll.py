from ..models import *
from rest_framework.decorators import api_view
from dotenv import load_dotenv
import os
from django.db.models import Sum


load_dotenv()



def calculate_net_salary(gross_salary,company):
    tax_rate = float(TaxRate.objects.filter(is_active=True,minimum_income__gte=gross_salary,maximum_income__lte=gross_salary).first().rate)
    deduction = float(Deduction.objects.filter(is_active=True,minimum_income__gte=gross_salary,maximum_income__lte=gross_salary).first().deduction)
    employment_income_tax = (gross_salary*tax_rate-deduction)
    pension = gross_salary*Pension.objects.filter(pension_type=company.company_type).first().employee_pension/100

    total_deduction = PayrollDeduction.objects.aggregate(total_deduction=Sum('amount'))['total_deduction'] or 0
    net_salary = gross_salary-employment_income_tax-total_deduction-float(pension)

    return net_salary
