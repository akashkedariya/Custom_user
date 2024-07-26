from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager 
from django.utils.translation import gettext_lazy as _



class Usermanager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):  
 
        if not email:  
            raise ValueError(('The Email must be Required'))  
        email = self.normalize_email(email)  
          
        user = self.model(email=email, **extra_fields)  
        user.set_password(password)  
        user.save(using=self._db)
        return user 
    

    def create_superuser(self, email, password, **extra_fields): 
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        extra_fields.setdefault('is_active', True) 

        if extra_fields.get('is_staff') is not True:  
            raise ValueError(('Superuser must have is_staff=True.'))
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50) 
    email = models.EmailField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = Usermanager()    


Designation= ( 
    ("Employee", "Employee"), 
    ("HR Manager", "HR Manager"),
    ("Senior Manager", "Senior Manager"), 
    ("Manager", "Manager"), 
    ("Assistant Manager", "Assistant Manager"), 
    ("Project Manager", "Project Manager"), 
    ("Team Leader", "Team Leader"), 
    ("Software Developer", "Software Developer"), 
    ("Interns/Trainees", "Interns/Trainees"), 
)

Department = (
    ('Python','Python'),
    ('React','React'),
    ('Php','Php'),
    ('IOS','IOS'),
    ('Flutter','Flutter')
)

class Register_employee(models.Model):
    # username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=30)
    emp_role = models.CharField( 
        max_length = 200, 
        choices = Designation, 
        default = 'Employee'
        ) 
    mobile_no = models.IntegerField()
    date_of_birth = models.DateField()
    department = models.CharField( 
        max_length = 200, 
        choices = Department, 
        default = ''
        ) 
    token = models.CharField(max_length=900)


    def __str__(self):
        return self.first_name
        # return f"{self.username},{self.emp_role}"


Department = (
    ('Python','Python'),
    ('React','React'),
    ('Php','Php'),
    ('IOS','IOS'),
    ('Flutter','flutter')
)
class Project(models.Model):

    # employee_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    department = models.CharField(max_length=200, choices=Department,default = '')
    # status = models.CharField(max_length=100,choices = STATUS, default = 'in progress')

    def __str__(self):
        return self.project_name
        # return int(self.id)

        # return f"{self.project_name},{self.department}"

    

status= ( 
    ("in_progress", "in_progress"), 
    ("completed", "completed"),
    ("submitted", "submitted"), 
)

priority= ( 
    ("Low", "Low"), 
    ("Medium", "Medium"),
    ("High", "High"), 
)

Department = (
    ('Python','Python'),
    ('React','React'),
    ('Php','Php'),
    ('IOS','IOS'),
    ('Flutter','flutter')
)

class Assign_task(models.Model):

    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    discription = models.CharField(max_length=500)
    assign_by = models.CharField(max_length=500)
    assign_to = models.ForeignKey(Register_employee,on_delete=models.CASCADE,null=True)
    department = models.CharField(max_length=100,choices = Department, 
        default = '')
    task_priority = models.CharField(max_length=100,choices = priority, 
        default = 'Low')
    task_assign_date = models.DateField()
    task_finish_date = models.DateField()
    task_status = models.CharField(max_length=100,choices = status, 
        default = 'in progress')    

