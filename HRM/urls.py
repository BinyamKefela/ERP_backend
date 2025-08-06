
from django.contrib import admin
from django.urls import path
from django.urls import include
from .api.user import *
from .api.group import *
from .api.permission import *
from .api.company import *
from .api.employee import *
from .api.department import *
from .api.position import *
from .api.work_history import *
from .api.attendance import *
from .api.leave import *
from .api.job_opening import *
from .api.applicant import *
from .api.performance_review import *
from .api.goal import *
from .api.document import *
from .api.training import *
from .api.training_attendance import *
from .api.employee_goal import *
from .api.payroll_calendar import *
from.api.payroll_period import *
from .api.overtime_policy import *
from .api.tax_rate import *
from .api.payroll_addition_type import *
from .api.payroll_addition import *
from .api.payroll_deduction_type import *
from .api.payroll_deduction import *
from .api.pension import *
from .api.payroll_policy import *
from .api.event import *
from .api.branch import *
from .api.transfer import *
from .api.termination import *
from .api.subscription_plan import *
from .api.subscription_payment import *
from .api.subscription_plan_service import *
from .api.subscription import *

urlpatterns = [

  #--------------------------------users routes-----------------------------------------------
  path("get_users", UserListView.as_view(), name="get_users"),
  path("get_user/<int:id>",UserRetrieveView.as_view(),name='get_user'),
  path("post_user",UserCreateView.as_view(),name="post_user"),
  path("update_user/<int:id>",update_user,name="new_update_user"),
  path("deactivate_user/<int:id>",UserDestroyView.as_view(),name="delete_user"),
  path("set_user_permissions",setUserPermissions,name="set_user_permissions"),
  path("set_user_groups", setUserGroups, name="set_user_group"),
  path("send_password_reset_email",send_password_reset_email,name="send_password_reset_email"),
  path("reset_password/<str:token>",reset_password,name="reset_passord"),
  path("get_user_profile",get_user_profile,name="get_user_id"),
  path("activate_user/<int:id>", activate_user, name="activate_user"),
  #path("get_owners",get_owners,name="get_owners"),
  #path("get_managers",get_managers,name="get_managers"),
  #path("get_owners",GetOwners.as_view(),name="get_owners"),

  path('auth/google', GoogleAuthView.as_view(), name='google_auth'),


  path('sign_up',sign_up, name='sign_up'),
  path('verify-email/<uuid:token>', verify_email, name='verify_email'),

  path('send_password_reset_email_phone',send_password_reset_email_phone, name='send_password_reset_email_phone'),
  path('verify_reset_code', VerifyResetCodeView.as_view(), name='verify_reset_code'),
  path('reset_password_phone',reset_password_phone,name='reset_password_phone'),

  path("change_password",change_password,name="change_password"),
  path("sign_up_company",sign_up_company,name="sign_up_company"),





  #--------------------------------Groups routes----------------------------------------------
  path("get_groups", GroupListView.as_view(), name="get_groups"),
  path("get_group/<int:id>",GroupRetrieveView.as_view(),name='get_group'),
  path("post_group",GroupCreateView.as_view(),name="post_group"),
  path("update_group/<int:id>",GroupUpdateView.as_view(),name="update_group"),
  path("delete_group/<int:id>",GroupDestroyView.as_view(),name="delete_group"),
  path("set_group_permissions",setGroupPermissions,name="set_group_permissions"),
  path("get_group_permissions",getGroupPermission,name="get_group_permissions"),



#--------------------------------Permission routes--------------------------------------------
  path("get_permissions", PermissionListView.as_view(), name="get_permissions"),
  path("get_permission/<int:id>",PermissionRetrieveView.as_view(),name='get_permission'),
  path("post_permission",PermissionCreateView.as_view(),name="post_permission"),
  path("update_permission/<int:id>",PermissionUpdateView.as_view(),name="update_permission"),
  path("delete_permission/<int:id>",PermissionDestroyView.as_view(),name="delete_permission"),

#-----------------------------------------Company routes-------------------------------------------

  path("get_companys", CompanyListView.as_view(), name="get_companys"),
  path("get_company/<int:id>",CompanyRetrieveView.as_view(),name='get_company'),
  path("post_company",CompanyCreateView.as_view(),name="post_company"),
  path("update_company/<int:id>",CompanyUpdateView.as_view(),name="update_company"),
  path("delete_company/<int:id>",CompanyDestroyView.as_view(),name="delete_company"),

  #-----------------------------------------Employee routes-------------------------------------------

  path("get_employees", EmployeeListView.as_view(), name="get_employees"),
  path("get_employee/<int:id>",EmployeeRetrieveView.as_view(),name='get_employee'),
  path("post_employee",EmployeeCreateView.as_view(),name="post_employee"),
  path("update_employee/<int:id>",EmployeeUpdateView.as_view(),name="update_employee"),
  path("delete_employee/<int:id>",EmployeeDestroyView.as_view(),name="delete_employee"),

  #-----------------------------------------Department routes-------------------------------------------

  path("get_departments", DepartmentListView.as_view(), name="get_departments"),
  path("get_department/<int:id>",DepartmentRetrieveView.as_view(),name='get_department'),
  path("post_department",DepartmentCreateView.as_view(),name="post_department"),
  path("update_department/<int:id>",DepartmentUpdateView.as_view(),name="update_department"),
  path("delete_department/<int:id>",DepartmentDestroyView.as_view(),name="delete_department"),


  #-----------------------------------------Position routes-------------------------------------------

  path("get_positions", PositionListView.as_view(), name="get_positions"),
  path("get_position/<int:id>",PositionRetrieveView.as_view(),name='get_position'),
  path("post_position",PositionCreateView.as_view(),name="post_position"),
  path("update_position/<int:id>",PositionUpdateView.as_view(),name="update_position"),
  path("delete_position/<int:id>",PositionDestroyView.as_view(),name="delete_position"),

   #-----------------------------------------Work history routes-------------------------------------------

  path("get_work_historys", WorkHistoryListView.as_view(), name="get_work_historys"),
  path("get_work_history/<int:id>",WorkHistoryRetrieveView.as_view(),name='get_work_history'),
  path("post_work_history",WorkHistoryCreateView.as_view(),name="post_workhistory"),
  path("update_work_history/<int:id>",WorkHistoryUpdateView.as_view(),name="update_work_history"),
  path("delete_work_history/<int:id>",WorkHistoryDestroyView.as_view(),name="delete_work_history"),


  #-----------------------------------------Attendance routes-------------------------------------------

  path("get_attendances",AttendanceListView.as_view(), name="get_attendances"),
  path("get_attendance/<int:id>",AttendanceRetrieveView.as_view(),name='get_attendance'),
  path("post_attendance",AttendanceCreateView.as_view(),name="post_attendance"),
  path("update_attendance/<int:id>",AttendanceUpdateView.as_view(),name="update_attendance"),
  path("delete_attendance/<int:id>",AttendanceDestroyView.as_view(),name="delete_attendance"),


  #-----------------------------------------Leave routes-------------------------------------------

  path("get_leaves", LeaveListView.as_view(), name="get_leaves"),
  path("get_leave/<int:id>",LeaveRetrieveView.as_view(),name='get_leave'),
  path("post_leave",LeaveCreateView.as_view(),name="post_leave"),
  path("update_leave/<int:id>",LeaveUpdateView.as_view(),name="update_leave"),
  path("delete_leave/<int:id>",LeaveDestroyView.as_view(),name="delete_leave"),


  #-----------------------------------------job opening routes-------------------------------------------

  path("get_job_openings", JobOpeningListView.as_view(), name="get_job_openings"),
  path("get_job_opening/<int:id>",JobOpeningRetrieveView.as_view(),name='get_job_opening'),
  path("post_job_opening",JobOpeningCreateView.as_view(),name="post_job_opening"),
  path("update_job_opening/<int:id>",JobOpeningUpdateView.as_view(),name="update_job_opening"),
  path("delete_job_opening/<int:id>",JobOpeningDestroyView.as_view(),name="delete_job_opening"),


   #-----------------------------------------applicant routes-------------------------------------------

  path("get_applicants", ApplicantListView.as_view(), name="get_applicants"),
  path("get_applicant/<int:id>",ApplicantRetrieveView.as_view(),name='get_applicant'),
  path("post_applicant",ApplicantCreateView.as_view(),name="post_applicant"),
  path("update_applicant/<int:id>",ApplicantUpdateView.as_view(),name="update_applicant"),
  path("delete_applicant/<int:id>",ApplicantDestroyView.as_view(),name="delete_applicant"),



   #-----------------------------------------performance review routes-------------------------------------------

  path("get_performance_reviews", PerformanceReviewListView.as_view(), name="get_performance_reviews"),
  path("get_performance_review/<int:id>",PerformanceReviewRetrieveView.as_view(),name='get_performance_review'),
  path("post_performance_review",PerformanceReviewCreateView.as_view(),name="post_performance_review"),
  path("update_performance_review/<int:id>",PerformanceReviewUpdateView.as_view(),name="update_performance_review"),
  path("delete_performance_review/<int:id>",PerformanceReviewDestroyView.as_view(),name="delete_performance_review"),


    #-----------------------------------------goal routes-------------------------------------------

  path("get_goals", GoalListView.as_view(), name="get_goals"),
  path("get_goal/<int:id>",GoalRetrieveView.as_view(),name='get_goal'),
  path("post_goal",GoalCreateView.as_view(),name="post_goal"),
  path("update_goal/<int:id>",GoalUpdateView.as_view(),name="update_goal"),
  path("delete_goal/<int:id>",GoalDestroyView.as_view(),name="delete_goal"),

  
   #-----------------------------------------Document routes-------------------------------------------

  path("get_documents", DocumentListView.as_view(), name="get_documents"),
  path("get_document/<int:id>",DocumentRetrieveView.as_view(),name='get_document'),
  path("post_document",DocumentCreateView.as_view(),name="post_document"),
  path("update_document/<int:id>",DocumentUpdateView.as_view(),name="update_document"),
  path("delete_document/<int:id>",DocumentDestroyView.as_view(),name="delete_document"),


   #-----------------------------------------training routes-------------------------------------------

  path("get_trainings", TrainingListView.as_view(), name="get_trainings"),
  path("get_training/<int:id>",TrainingRetrieveView.as_view(),name='get_training'),
  path("post_training",TrainingCreateView.as_view(),name="post_training"),
  path("update_training/<int:id>",TrainingUpdateView.as_view(),name="update_training"),
  path("delete_training/<int:id>",TrainingDestroyView.as_view(),name="delete_training"),


     #-----------------------------------------training attendance routes-------------------------------------------

  path("get_training_attendances", TrainingAttendanceListView.as_view(), name="get_training_attendances"),
  path("get_training_attendance/<int:id>",TrainingAttendanceRetrieveView.as_view(),name='get_training_attendance'),
  path("post_training_attendance",TrainingAttendanceCreateView.as_view(),name="post_training_attendance"),
  path("update_training_attendance/<int:id>",TrainingAttendanceUpdateView.as_view(),name="update_training_attendance"),
  path("delete_training_attendance/<int:id>",TrainingAttendanceDestroyView.as_view(),name="delete_training_attendance"),

     #-----------------------------------------employee goal routes-------------------------------------------

  path("get_employee_goals", EmployeeGoalListView.as_view(), name="get_employee_goals"),
  path("get_employee_goal/<int:id>",EmployeeGoalRetrieveView.as_view(),name='get_employee_goal'),
  path("post_employee_goal",EmployeeGoalCreateView.as_view(),name="post_employee_goal"),
  path("update_employee_goal/<int:id>",EmployeeGoalUpdateView.as_view(),name="update_employee_goal"),
  path("delete_employee_goal/<int:id>",EmployeeGoalDestroyView.as_view(),name="delete_employee_goal"),


     #-----------------------------------------payroll calendar routes-------------------------------------------

  path("get_payroll_calendars", PayrollCalendarListView.as_view(), name="get_payroll_calendars"),
  path("get_payroll_calendar/<int:id>",PayrollCalendarRetrieveView.as_view(),name='get_payroll_calendar'),
  path("post_payroll_calendar",PayrollCalendarCreateView.as_view(),name="post_payroll_calendar"),
  path("update_payroll_calendar/<int:id>",PayrollCalendarUpdateView.as_view(),name="update_payroll_calendar"),
  path("delete_payroll_calendar/<int:id>",PayrollCalendarDestroyView.as_view(),name="delete_payroll_calendar"),



       #-----------------------------------------payroll calendar routes-------------------------------------------

  path("get_payroll_periods", PayrollPeriodListView.as_view(), name="get_payroll_periods"),
  path("get_payroll_period/<int:id>",PayrollPeriodRetrieveView.as_view(),name='get_payroll_period'),
  path("post_payroll_period",PayrollPeriodCreateView.as_view(),name="post_payroll_period"),
  path("update_payroll_period/<int:id>",PayrollPeriodUpdateView.as_view(),name="update_payroll_period"),
  path("delete_payroll_period/<int:id>",PayrollPeriodDestroyView.as_view(),name="delete_payroll_period"),


  #-----------------------------------------overtime policy routes-------------------------------------------

  path("get_overtime_policys", OvertimePolicyListView.as_view(), name="get_overtime_policys"),
  path("get_overtime_policy/<int:id>",OvertimePolicyRetrieveView.as_view(),name='get_overtime_policy'),
  path("post_overtime_policy",OvertimePolicyCreateView.as_view(),name="post_overtime_policy"),
  path("update_overtime_policy/<int:id>",OvertimePolicyUpdateView.as_view(),name="update_overtime_policy"),
  path("delete_overtime_policy/<int:id>",OvertimePolicyDestroyView.as_view(),name="delete_overtime_policy"),

  #-----------------------------------------tax rate routes-------------------------------------------
  path("get_tax_rates", TaxRateListView.as_view(), name="get_tax_rates"),
  path("get_tax_rate/<int:id>", TaxRateRetrieveView.as_view(), name='get_tax_rate'),
  path("post_tax_rate", TaxRateCreateView.as_view(), name="post_tax_rate"),
  path("update_tax_rate/<int:id>", TaxRateUpdateView.as_view(), name="update_tax_rate"),
  path("delete_tax_rate/<int:id>", TaxRateDestroyView.as_view(), name="delete_tax_rate"),


  #-----------------------------------------payroll addition type routes-------------------------------------------
  path("get_payroll_addition_types", PayrollAdditionTypeListView.as_view(), name="get_payroll_addition_types"),
  path("get_payroll_addition_type/<int:id>", PayrollAdditionTypeRetrieveView.as_view(), name='get_payroll_addition_type'),
  path("post_payroll_addition_type", PayrollAdditionTypeCreateView.as_view(), name="post_payroll_addition_type"),
  path("update_payroll_addition_type/<int:id>", PayrollAdditionTypeUpdateView.as_view(), name="update_payroll_addition_type"),
  path("delete_payroll_addition_type/<int:id>", PayrollAdditionTypeDestroyView.as_view(), name="delete_payroll_addition_type"), 
  
  #-----------------------------------------payroll addition routes-------------------------------------------
  path("get_payroll_additions", PayrollAdditionListView.as_view(), name="get_payroll_additions"),
  path("get_payroll_addition/<int:id>", PayrollAdditionRetrieveView.as_view(), name='get_payroll_addition'),
  path("post_payroll_addition", PayrollAdditionCreateView.as_view(), name="post_payroll_addition"),
  path("update_payroll_addition/<int:id>", PayrollAdditionUpdateView.as_view(), name="update_payroll_addition"),
  path("delete_payroll_addition/<int:id>", PayrollAdditionDestroyView.as_view(), name="delete_payroll_addition"),

  #-----------------------------------------payroll deduction type routes-------------------------------------------
  path("get_payroll_deduction_types", PayrollDeductionTypeListView.as_view() , name="get_payroll_deduction_types"),
  path("get_payroll_deduction_type/<int:id>", PayrollDeductionTypeRetrieveView.as_view(), name='get_payroll_deduction_type'),
  path("post_payroll_deduction_type", PayrollDeductionTypeCreateView.as_view(), name="post_payroll_deduction_type"),
  path("update_payroll_deduction_type/<int:id>", PayrollDeductionTypeUpdateView.as_view(), name="update_payroll_deduction_type"),
  path("delete_payroll_deduction_type/<int:id>", PayrollDeductionTypeDestroyView.as_view(), name="delete_payroll_deduction_type"),  
  

  #-----------------------------------------payroll deduction routes-------------------------------------------
  path("get_payroll_deductions", PayrollDeductionListView.as_view(), name="get_payroll_deductions"),
  path("get_payroll_deduction/<int:id>", PayrollDeductionRetrieveView.as_view(), name='get_payroll_deduction'),
  path("post_payroll_deduction", PayrollDeductionCreateView.as_view(), name="post_payroll_deduction"),
  path("update_payroll_deduction/<int:id>", PayrollDeductionUpdateView.as_view(), name="update_payroll_deduction"),
  path("delete_payroll_deduction/<int:id>", PayrollDeductionDestroyView.as_view(), name="delete_payroll_deduction"),


  #-----------------------------------------Pension routes-------------------------------------------
  path("get_pensions", PensionListView.as_view(), name="get_pensions"),
  path("get_pension/<int:id>", PensionRetrieveView.as_view(), name='get_pension'),
  path("post_pension", PensionCreateView.as_view(), name="post_pension"),
  path("update_pension/<int:id>", PensionUpdateView.as_view(), name="update_pension"),
  path("delete_pension/<int:id>", PensionDestroyView.as_view(), name="delete_pension"),


  #-----------------------------------------Payroll Policy routes-------------------------------------------
  path("get_payroll_policys", PayrollPolicyListView.as_view(), name="get_payroll_policys"),
  path("get_payroll_policy/<int:id>", PayrollPolicyRetrieveView.as_view(), name='get_payroll_policy'),
  path("post_payroll_policy", PayrollPolicyCreateView.as_view(), name="post_payroll_policy"),
  path("update_payroll_policy/<int:id>", PayrollPolicyUpdateView.as_view(), name="update_payroll_policy"),
  path("delete_payroll_policy/<int:id>", PayrollPolicyDestroyView.as_view(), name="delete_payroll_policy"),

 
  #-----------------------------------------Event routes-------------------------------------------
  path("get_events", EventListView.as_view(), name="get_events"),
  path("get_event/<int:id>", EventRetrieveView.as_view(), name='get_event'),
  path("post_event", EventCreateView.as_view(), name="post_event"),
  path("update_event/<int:id>", EventUpdateView.as_view(), name="update_event"),
  path("delete_event/<int:id>", EventDestroyView.as_view(), name="delete_event"),

  #-----------------------------------------Branch routes-------------------------------------------
  path("get_branches", BranchListView.as_view(), name="get_branches"),
  path("get_branch/<int:id>", BranchRetrieveView.as_view(), name='get_branch'),
  path("post_branch", BranchCreateView.as_view(), name="post_branch"),
  path("update_branch/<int:id>", BranchUpdateView.as_view(), name="update_branch"),
  path("delete_branch/<int:id>", BranchDestroyView.as_view(), name="delete_branch"),


  #-----------------------------------------transfer routes-------------------------------------------
  path("get_transfers", TransferListView.as_view(), name="get_transfers"),
  path("get_transfer/<int:id>", TransferRetrieveView.as_view(), name='get_transfer'),
  path("post_transfer", TransferCreateView.as_view(), name="post_transfer"),
  path("update_transfer/<int:id>", TransferUpdateView.as_view(), name="update_transfer"),
  path("delete_transfer/<int:id>", TransferDestroyView.as_view(), name="delete_transfer"),


  #-----------------------------------------termination routes-------------------------------------------
  path("get_terminations", TerminationListView.as_view(), name="get_terminations"),
  path("get_termination/<int:id>", TerminationRetrieveView.as_view(), name='get_termination'),
  path("post_termination", TerminationCreateView.as_view(), name="post_termination"),
  path("update_termination/<int:id>", TerminationUpdateView.as_view(), name="update_termination"),
  path("delete_termination/<int:id>", TerminationDestroyView.as_view(), name="delete_termination"),

  #-----------------------------------------Subscription Plan routes-------------------------------------------
  path("get_subscription_plans", SubscrptionPlanListView.as_view(), name="get_subscription_plans"),
  path("get_subscription_plan/<int:id>", SubscrptionPlanRetrieveView.as_view(), name='get_subscription_plan'),
  path("post_subscription_plan", create_subscription_plan, name="post_subscription_plan"),
  path("update_subscription_plan/<int:id>", SubscrptionPlanUpdateView.as_view(), name="update_subscription_plan"),
  path("delete_subscription_plan/<int:id>", SubscrptionPlanDestroyView.as_view(), name="delete_subscription_plan"),

  #-----------------------------------------Subscription Payment routes-------------------------------------------
  path("get_subscription_payments", SubscriptionPaymentListView.as_view(), name="get_subscription_payments"),
  path("get_subscription_payment/<int:id>", SubscriptionPaymentRetrieveView.as_view(), name='get_subscription_payment'),
  path("post_subscription_payment", SubscriptionPaymentCreateView.as_view(), name="post_subscription_payment"),
  path("update_subscription_payment/<int:id>", SubscriptionPaymentUpdateView.as_view(), name="update_subscription_payment"),
  path("delete_subscription_payment/<int:id>", SubscriptionPaymentDestroyView.as_view(), name="delete_subscription_payment"),

  #------------------------------------------Subscription Plan Service routes---------------------------------------------


  path("get_subscription_plan_service", SubscriptionPlanServiceListView.as_view(), name="get_subscription_plan_service"),
  path("get_subscription_plan_service/<int:id>", SubscriptionPlanServiceRetrieveView.as_view(), name='get_subscription_plan_service'),
  path("post_subscription_plan_service", SubscriptionPlanServiceCreateView.as_view(), name="post_subscription_plan_service"),
  path("update_subscription_plan_service/<int:id>", SubscriptionPlanServiceUpdateView.as_view(), name="update_subscription_plan_service"),
  path("delete_subscription_plan_service/<int:id>",SubscriptionPlanServiceDestroyView.as_view(), name="delete_subscription_plan_service"),

  #-----------------------------------------Subscription routes-------------------------------------------------------

  path("get_subscription", SubscriptionListView.as_view(), name="get_subscription_plan_service"),
  path("get_subscription/<int:id>", SubscriptionRetrieveView.as_view(), name='get_subscription_plan_service'),
  path("post_subscription", SubscriptionCreateView.as_view(), name="post_subscription_plan_service"),
  path("update_subscription/<int:id>", SubscriptionUpdateView.as_view(), name="update_subscription_plan_service"),
  path("delete_subscription/<int:id>",SubscriptionDestroyView.as_view(), name="delete_subscription_plan_service"),


]
