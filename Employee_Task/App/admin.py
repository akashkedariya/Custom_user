from django.contrib import admin
from.models import CustomUser, Register_employee, Project, Assign_task
# Register your models here.




@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','is_active','is_superuser','email','password']


@admin.register(Register_employee)
class register_employeeAdmin(admin.ModelAdmin):
    list_display = [ 'id','first_name','last_name','full_name','email','emp_role','mobile_no','date_of_birth','department','token' ]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [ 'id','project_name','description','department' ]


@admin.register(Assign_task)
class Assign_taskAdmin(admin.ModelAdmin):
    list_display = [ 'id','project_name','discription','assign_by','assign_to','department','task_priority','task_assign_date','task_finish_date','task_status' ]
