from django.contrib import admin
from .models import candidate, human_resources, job, candidate_account, department, background_images,CV
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# Register your models here.

admin.site.site_header = "Admin Panel"
admin.site.site_title = "HR Admin Panel"

def register_candidate(modeladmin, request, queryset): #to allow candidate to login - an action is created to transfer candidate data in user.auth
    for candidate in queryset:
        if candidate.username is not None and candidate.password is not None:
            username = candidate.username
            password = candidate.password
            email = candidate.email
            newuser = User.objects.create_user(username, email, password)
            newuser.first_name = candidate.fname
            newuser.last_name = candidate.lname
            newuser.save()

            email = EmailMessage(
                'Welcome to Madkour Group',
                render_to_string('email.html', {
                    'fname': candidate.fname,
                    'lname': candidate.lname,
                    'username': username,
                    'password': password,
                }),
                settings.EMAIL_HOST_USER,
                [newuser.email],
            )
            email.fail_silently = False
            email.send()
        else:
            messages.error(request, 'Insert Username & Password')

def notify_candidate(candidate):
    if candidate.cand_status == 'accepted':
        message = 'We are pleased to inform you that you have been accepted. Please login to your account to learn more.'
    elif candidate.cand_status == 'rejected':
        message = 'We are sorry to inform you that you have been rejected. Please login to your account to learn more.'
    elif candidate.cand_status == 'on stack':
        message = 'We are sorry to inform you that you have been put on stack. Please login to your account to learn more.'
    else:
        return
    email = EmailMessage(
        'Welcome to Madkour Group',
        'Dear '+ candidate.fname + ' ' + candidate.lname + ',\n' + message,
        settings.EMAIL_HOST_USER,
        [candidate.email],
    )
    email.fail_silently = False
    email.send()
            
    
@admin.register(human_resources) 
class human_resources(admin.ModelAdmin):
    pass

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    fields=('title','description','depName','depID','HR_code','applicants_count','level','work_arrangement','salary', 'years_of_experience', 'location', 'is_active')
    list_display = ('title', 'depName','applicants_count', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'depName', 'level', 'work_arrangement', 'location', 'salary', 'years_of_experience')
    
    

@admin.register(candidate_account)
class CandidateAccountAdmin(admin.ModelAdmin):
    fields=('username','password','candID.email')
    list_display = ('username', 'candID')
    actions = [register_candidate]

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    fields=('depName',)
    list_display=('depName',)
    
@admin.register(background_images)
class BackgroundImagesAdmin(admin.ModelAdmin):
    fields=('homepage','jobs','application','thank_you','logout','login','account')
    list_display=('homepage','jobs','application','thank_you','logout','login','account')

@admin.register(candidate)
class candAdmin(admin.ModelAdmin):
    fields = ('cv','fname', 'lname','address','military_status','phone','dob', 'age','cand_status','email','title','jobID','password', 'username','Note','To_Candidate')
    list_display = ('email','fname', 'lname','title','cv','cand_status')  #to display column 
    list_editable = ('cand_status',)
    list_display_links=('email',)
    list_filter=('cand_status','title')
    search_fields=('fname','lname','email','dob')
    actions = [register_candidate]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['fname', 'lname', 'address', 'phone', 'dob', 'email', 'jobID', 'age', 'military_status', 'cv', 'title']
        else:
            return []
        
    # check if the status is changed
    def save_model(self, request, obj, form, change):
        if change:
            if obj.cand_status != form.initial['cand_status']:
                notify_candidate(obj)
        obj.save()
    
                

        
    
    
    
""" def title():
       ID= candidate.jobID
       title = job.objects.get(jobID=ID)
       return title"""
    
       

    


  
