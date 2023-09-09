from django.contrib import admin, messages
from .models import candidate, human_resources, job, candidate_account, department, background_images,resume
from django.contrib.auth.models import User, Group 
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django import forms
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver




# Register your models here.

admin.site.site_header = "Admin Panel"
admin.site.site_title = "HR Admin Panel"

@receiver(post_save, sender=job)
@receiver(post_delete, sender=job)
def update_jobs_count(sender, instance, **kwargs):
    department_id = instance.depID_id
    dep = department.objects.get(pk=department_id)
    dep.jobs_count = job.objects.filter(depID_id=department_id).count()
    dep.save()



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


def Add_HR_Account(modeladmin, request, queryset):
    for human_resources in queryset:
        if human_resources.username is not None and human_resources.password is not None:
            username = human_resources.username
            password = human_resources.password
            email = "none"
           
            newuser = User.objects.create_user(username,email ,password)
            newuser.first_name = human_resources.username
            newuser.save()

           
    
@admin.register(human_resources) 
class human_resources(admin.ModelAdmin):
    fields = ('username','password')
    list_display = ('username', )
    
    actions=[Add_HR_Account]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username', 'HR_code']
        else:
            return []
            
   

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    fields=('title','description','depID','HR_code','applicants_count','level','work_arrangement','salary', 'years_of_experience', 'location', 'is_active')
    list_display = ('title', 'depID','applicants_count', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'depID', 'level', 'work_arrangement', 'location', 'salary', 'years_of_experience')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['applicants_count', 'depID']
        else:
            return []
    

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    fields=('depName','jobs_count')
    list_display=('depName','number_of_applied','jobs_count')
    
    def number_of_applied(self, obj):
        count = job.objects.filter(depName=obj.depName).count()  # Count jobs with matching department name
        return count

    number_of_applied.short_description = 'Applied candidates'
    
@admin.register(background_images)
class BackgroundImagesAdmin(admin.ModelAdmin):
    fields=('homepage','jobs','application','thank_you','logout','login','account')
    list_display=('homepage','jobs','application','thank_you','logout','login','account')
    
    
    
    
class CustomCandForm(forms.ModelForm):
    class Meta:
        model = candidate
        fields = '__all__'
        widgets = {
            'password': forms.HiddenInput(),  # Set the widget for password field
        }


@admin.register(candidate)
class candAdmin(admin.ModelAdmin):
    fields = ('cv','auto_resume','fname', 'lname','address','military_status','phone','dob', 'age','cand_status','email','jobID','depID','username','password','Note','To_Candidate')
    list_display = ('email','fname', 'lname','jobID','cv','cand_status')  #to display column 
    list_editable = ('cand_status',)
    list_display_links=('email',)
    list_filter=('cand_status','jobID','depID')
    search_fields=('fname','lname','email','dob')
    actions = [register_candidate]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.groups.filter(name='viewer').exists():
            print('viewer')
            return CustomCandForm
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['fname', 'lname', 'address', 'phone', 'dob', 'email', 'jobID', 'depID', 'age', 'military_status', 'cv', 'title', 'auto_resume']
        else:
            return []
        
    # check if the status is changed
    def save_model(self, request, obj, form, change):
        if change:
            if obj.cand_status != form.initial['cand_status']:
                notify_candidate(obj)
        obj.save()
   
        
        
    
                

admin.site.unregister(User)
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ( 'first_name', 'last_name', 'email', 'username','display_groups')
    list_filter=('groups',)

    def display_groups(self, obj):
        groups = obj.groups.all()  # Get the groups associated with the user
        if groups:
            return ', '.join(group.name for group in groups)
        else:
            return 'Candidate'  # Display "Candidate" if user has no groups

    display_groups.short_description = 'permission level'
    

    
       

    


  