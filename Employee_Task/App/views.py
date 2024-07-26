from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Register_employee, Assign_task, Project, CustomUser
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
import jwt


@csrf_exempt
def register_employee(request):
    if request.method == 'POST':

        # last_emp = User.objects.last()
        # print('====last_emp======',last_emp]
        first_name = request.POST['first_name']
        username = first_name 
        last_name = request.POST['last_name']
        email = request.POST.get('email')
        full_name = request.POST['full_name']
        mobile_no = request.POST['mobile_no']
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        emp_role = request.POST.get('emp_role')
        date_of_birth = request.POST.get('date_of_birth')
        department = request.POST.get('department')

        data = CustomUser.objects.filter(email=email)

        if data:
            return JsonResponse({'email':'Already Registered email'})
        else:

            if password == confirm_password:
                user = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name, email=email, password=password) 
                user.set_password(password)
                user.save()

                encoded_jwt = jwt.encode({'email': email,'id':user.id}, 'secret', algorithm='HS256')
                
                data2 = Register_employee.objects.create(token=encoded_jwt,first_name=first_name,full_name=full_name,mobile_no=mobile_no,last_name=last_name, email=email,department=department, emp_role=emp_role,date_of_birth=date_of_birth)
                data2.save()

                data_list =[]
                dict = {
                        'first_name':first_name,
                        # username = first_name 
                        'last_name':last_name,
                        'full_name' : full_name,
                        'email' : email,
                        "mobile_no" : mobile_no,
                        "emp_role" : emp_role,
                        "date_of_birth" : date_of_birth,
                        "department" : department
                    }

                data_list.append(dict)

                return JsonResponse({'Employee':'Employee data Registered','Registered Data' : data_list})
            else:
                return JsonResponse({'password':'password not match'})

    else:
        return JsonResponse({'user':'Enter valid method'}) 
    

@csrf_exempt        
def login(request):
   
    if request.method == 'POST':

        try:
            email = request.POST.get('email')
            password1 = request.POST.get('password')

            data = CustomUser.objects.get(email=email) 
            checkpassword=check_password(password1,data.password)
            request.session['email'] = data.email
            sesion = request.session['email']

            if checkpassword == True:
                # try:
                print("in 2nd tru")
                request.session['email'] = data.email
                encoded_jwt2 = jwt.encode({'email': data.email,'id':data.id}, 'secret', algorithm='HS256')
                data1 = CustomUser.objects.get(email=email)
                data2 = Register_employee.objects.filter(email=data1.email)
            
                for i in data2:
                    v = i.token

                if str(encoded_jwt2) == str(v):
                    # session_time = request.session.set_expiry(15)       # login expire in 15 second   ,,'session_time':session_time
                    return JsonResponse({'User Email':sesion,'Token':v,'Login':'Successfully login'},status = 200)
                else:
                
                    return JsonResponse({"Token":'Not matched Token...'})
                # except:
            else:
                return JsonResponse({"data":'Invalid email-password'})    

        except:
            return JsonResponse({"data":'Invalid email-password'})

    else:
        return JsonResponse({"data":'Invalid method'})    

    

@csrf_exempt
def logout(request):
   if request.method == 'POST':
        try:
            del request.session['email']
        except:
            pass
        return JsonResponse({'Logout':'user logout'})     
    
import json

@csrf_exempt
def assign_task(request):
    if request.method == 'POST':
        
        if request.session.get('email'):
            user_data = Register_employee.objects.get(email = request.session.get('email'))
        
            if user_data.emp_role == 'Project Manager' or user_data.emp_role == 'Team Leader':

                project_name = request.POST['project_name']
                
                discription = request.POST['discription']
                assign_by = user_data
                assign_to = request.POST['assign_to']

                pro_name = Project.objects.get(id=project_name)
                print('=======pro_name===assigne_to=======',pro_name)

                # department = request.POST.get('department')
                department = pro_name.department
                task_priority = request.POST.get('task_priority')
                task_assign_date = request.POST.get('task_assign_date')
                task_finish_date = request.POST.get('task_finish_date')
                task_status = request.POST.get('task_status')


                # assi_user = Register_employee.objects.get(id=assign_to)
                # task_user = Assign_task.objects.filter(assign_to=assi_user)

                # for i in task_user:
                
                #     if i.assign_to == assi_user:
                    
                #         aa = datetime.strptime(task_assign_date,'%Y-%m-%d').date()

                #         if i.task_assign_date <= aa <= i.task_finish_date :
                        
                #             dict = {'Date':aa,'Task' :'Task already assigned this date' }
                #             return JsonResponse({'dict':dict},safe=False)
                
                assi_to = Register_employee.objects.get(id=assign_to)
         
                Assign_task.objects.create(project_name=pro_name,discription=discription,assign_by=assign_by, assign_to=assi_to,department=department, task_priority=task_priority,task_assign_date=task_assign_date,task_finish_date=task_finish_date,task_status=task_status)
              
                dict = {
                    "project_name" : str(pro_name.project_name),
                    "discription" : discription,
                    "assign_by" : str(user_data.first_name),
                    "assign_to" : str(assi_to.first_name), 
                    "department" : str(pro_name.department),
                    "task_priority" : task_priority,
                    "task_assign_date" : task_assign_date,
                    "task_finish_date" : task_finish_date,
                    "task_status" : task_status
                }
             
                return JsonResponse({'Assign_task':'Task assigned successfully',"Data":dict}) 

            else:
                return JsonResponse({'Role' : 'Your role have no permission to assign task '})    

        else:
            return JsonResponse({'Login' : ' User is not logged in '})

    # return JsonResponse({'Assign_task':'Task assigned successfully....'}) 
    

@csrf_exempt
def task_update(request):
   
    if request.method == 'POST': 
        task_id = request.POST.get('task_id')
       
        if request.session.get('email'):
            user_data = Register_employee.objects.get(email = request.session.get('email'))

            if user_data.emp_role == 'Project Manager' or user_data.emp_role == 'Team Leader':

                data = Assign_task.objects.get(id=task_id)
               
                project_id = Project.objects.get(id=request.POST['project_name'])
              
                data.project_name = project_id    #ID
                data.discription = request.POST['discription']
                data.assign_by = str(user_data)
                assign_id = Register_employee.objects.get(id=request.POST['assign_to'])
              
                data.assign_to = assign_id          #ID
                data.department = request.POST.get('department')
                data.task_priority = request.POST.get('task_priority')
                data.task_assign_date = request.POST.get('task_assign_date')
                print('=========================',type(request.POST.get('task_assign_date')))
                data.task_finish_date = request.POST.get('task_finish_date')
                data.task_status = request.POST.get('task_status')

                data.save()   

                dict = {
                    "project_name" : str(project_id.project_name),
                    "discription" : data.discription,
                    "assign_by" : str(user_data.first_name),
                    "assign_to" : str(assign_id.first_name), 
                    "department" : data.discription,
                    "task_priority" : data.task_priority,
                    "task_assign_date" : data.task_assign_date,
                    "task_finish_date" : data.task_finish_date,
                    "task_status" : data.task_status
                } 

                return JsonResponse({'Data':'Data is updated',"Updated Assigned data  ":dict})   
            
            # elif user_data.emp_role == 'Software_Developer':
            #     data = Assign_task.objects.get(id=task_id)
            #     print('====data updated======',data.project_name)                
            #     data.task_assign_date = request.POST.get('task_assign_date')
            #     data.task_finish_date = request.POST.get('task_finish_date')
            #     data.task_status = request.POST.get('task_status')
            #     data.save()

                # return JsonResponse({'data':'Data is update by Software_Developer'}) 

            else:

                return JsonResponse({'User': 'User is not valid '})     
            
        else:
            return JsonResponse({'Login' : ' User is not logged in '})    


@csrf_exempt
def task_delete(request):
        
    if request.method == 'POST':    #if request.method == 'DELETE':
       
        task_id = request.POST.get('task_id')
        data = Assign_task.objects.get(id=task_id)
        assigned_task = data       
        data.delete()   

    return JsonResponse({'Data':'Assigned task deleted',"Deleted assigned_task" : str(assigned_task.project_name)})
        

@csrf_exempt
def employee_task(request):
    if request.method == 'POST':
       
        task_id = request.POST.get('task_id')
        print('-==========task_id==============',task_id)
        
        if task_id is not None: 
            data = Assign_task.objects.get(id=task_id)

            pro_name = str(data.project_name)
            assi_name = str(data.assign_to)

            dict = {'id':data.id,'project_name':pro_name,'department':data.department,'assign_by':data.assign_by,'assign_to':assi_name,'department':data.department,"task_priority":data.task_priority,'task_assign_date':data.task_assign_date,'task_finish_date':data.task_finish_date,'task_status':data.task_status}
 
            return JsonResponse({'dict':dict},safe=False)
            # return JsonResponse({'id':data.id, 'project_name':data.project_name, 'assignee':data.assignee, 'assigne_to':data.assigne_to,'department':data.department,'task_assign_date':data.task_assign_date,'task_finish_date':data.task_finish_date,'task_status':data.task_status},safe=False)

        else:
            
            data1 = list(Assign_task.objects.values())   

            return JsonResponse(data1,safe=False)
        

@csrf_exempt
def project_register(request):
    if request.method == 'POST':

        if request.session.get('email'):
            user_data = Register_employee.objects.get(email = request.session.get('email'))

            if user_data.emp_role == 'Project Manager' or user_data.emp_role == 'Team Leader':

                project_name = request.POST['project_name']
                description = request.POST['description']
                department = request.POST['department']
                user = Project.objects.create(project_name=project_name,description=description,department=department)
                user.save()

                dict = {
                    "project_name" : project_name,
                    "description" : description,
                    "department" : department

                }

                return JsonResponse({'Project':'Project Registred',"Project Data" : dict})
            else:
                
                return JsonResponse({'User':'User not valid'})   
            
        else:
            return JsonResponse({'Login' : ' User is not login '})



@csrf_exempt
def employee_department_wise(request):     #   J 
    try:
        list = []
        if request.method == 'POST':
            # department = request.GET.get('department')
            department = request.POST['department']
            fetch_data = Register_employee.objects.all()
            for i in fetch_data:
                if department == i.department:
                    print('=========i.department=======',i.first_name)
                    dict = {
                        "first_name":i.first_name,
                        "last_name":i.last_name,
                        "full_name":i.full_name,
                        "email":i.email,
                        "emp_role":i.emp_role,
                        "date_of_birth":i.date_of_birth,
                        "mobile_no":i.mobile_no,
                        "department":i.department,
                        
                        }
                    list.append(dict)           

        return JsonResponse({'Status':'Success','Message':'Data Fetched.','Data':list},safe=False,status = 200)
    
    except Exception as e:
        return JsonResponse({'status':'Failure','message':str(e)},status = 400)
    


@csrf_exempt
def employee_task_user(request):  # J
    
    if request.method == 'POST':
       
        emp_id = request.POST.get('emp_id')
        data = Register_employee.objects.get(id=emp_id)
    
        fetch_data = Assign_task.objects.all()
        list = []
        for emp_name in fetch_data:
        
            if data == emp_name.assign_to :
                print(emp_name.assign_to,'=======',emp_name.project_name)

                project_name = str(emp_name.project_name)
                assign_to = str(emp_name.assign_to)

                dict = {
                "assign_to":assign_to,
                "project_name":project_name,
                "assign_by":emp_name.assign_by,
                "task_assign_date":emp_name.task_assign_date,
                "task_finish_date":emp_name.task_finish_date,
                }
                list.append(dict)

    return JsonResponse({'Employee task ':list},safe=False)

    

@csrf_exempt
def project_data_show(request):  # J 
    try:
        if request.method == 'GET':
            list = []
            fetch_data = Project.objects.all()
            for i in fetch_data:
                dict = {
                    "project_name":i.project_name,
                    "description":i.description,
                    "department":i.department
                }
                list.append(dict)
            return JsonResponse({'Status':'Success','Message':'Project Data','Data':list},status = 200)
        
    except Exception as e:
        return JsonResponse({'status':'Failure','message':str(e)},status = 400)   

# sssssssnnnnn

@csrf_exempt
def project_data_dep(request):
    data =[]
    print(request)
    if request.method == 'POST':
        user = CustomUser.objects.get(email=request.session['email'])
        emp = Register_employee.objects.get(email=user.email)

        if emp.emp_role == 'Project Manager':
            dep = request.POST.get('dep')
            projects = Project.objects.filter(department=dep)
            for i in projects:
                dict = {
                "project_name":i.project_name,
                "description":i.description,
                "department":i.department
                }
                data.append(dict)
                
            return JsonResponse({"data":data})
        else:
            return JsonResponse({"data":"You are not authorized"})
    else:
        return JsonResponse({"data" : "not valid method"})
      


@csrf_exempt
def project_assign_user(request):
    
    if request.method == 'POST':
        project = request.POST['project']
        emp = Assign_task.objects.get(id=project)
        # print('==========emp==========',type(emp.project_name))
        assign_user = Assign_task.objects.all()

        data = []
        for user in assign_user:
           
            if str(user.project_name) == str(emp.project_name):
                print('==00====',user.assign_to)
                  
                dict = {
                "project_name" :str(user.project_name),
                "assign_by":user.assign_by,
                "assign_to":str(user.assign_to),
                "task_assign_date":user.task_assign_date,
                "task_priority":user.task_priority,
                "task_status":user.task_status,
                }
                data.append(dict)

        print('==33====',data)
        return JsonResponse({"Project data":data})
    
 


    #     emp = Assign_task.objects.filter(project_id=project).values()
    #     assign_to_ids = [task['assign_to_id'] for task in emp]
    #     for i in assign_to_ids:
    #         emps = Register_employee.objects.get(id=i)
    #         dict = {
    #             "assign_to":emps.first_name,
    #         }
    #         data.append(dict)
    #     return JsonResponse({"data" : data})
    # else:
    #     return JsonResponse({"data" : "request method not valid "})


# @csrf_exempt
# def add_project(request):
#     user = User.objects.get(email=request.session['email'])
#     emp = Register_employee.objects.get(user_id=user)
#     if emp.role == 'manager':
#         if request.POST:
#             project_name = request.POST.get('project_name')
#             description = request.POST.get('description')
#             department = request.POST.get('department')
#             Project.objects.create(
#                 project_name = project_name,
#                 description = description,
#                 department = department
#             )
#             return JsonResponse({"data":"Project Added"})
#         else:
#             return JsonResponse({"data":"Project add page"})
#     else:
#         return JsonResponse({"data":"You are not authorized"})



