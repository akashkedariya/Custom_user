from django.urls import path
from . import views





urlpatterns=[
    path('register_employee/',views.register_employee),
    path('assign_task/',views.assign_task),
    path('employee_task/',views.employee_task),
    path('project_register/',views.project_register),
    path('update/',views.task_update),
    path('delete/',views.task_delete),
    path('log_in/',views.login),
    path('logout/',views.logout),

    path('employee_department_wise/',views.employee_department_wise),
    path('employee_task_user/',views.employee_task_user),
    path('project_data_show/',views.project_data_show),

    # path("add_project/",add_project),
    path("project_data_dep/",views.project_data_dep),
    path("project_assign_user/" ,views.project_assign_user)  



]