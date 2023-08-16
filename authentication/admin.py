from django.contrib import admin
from .models import candidate, human_resources, job, candidate_account, department

# Register your models here.
@admin.register(candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass

@admin.register(human_resources)
class HumanResourcesAdmin(admin.ModelAdmin):
    pass

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    pass

@admin.register(candidate_account)
class CandidateAccountAdmin(admin.ModelAdmin):
    pass

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    pass



class canddis(admin.ModelAdmin):
    fields = ('cv','fname','address','military_status','phone','dob','cand_status')
    list_display = ('fname','military_status','cv','cand_status')  #to display column 
    list_display_links=('fname',)
    list_editable=('cand_status',)  
    list_filter=('cand_status',)
    search_fields=('fname','dob')
    
    
    
admin.site.register(candAccount)
admin.site.register(cands,canddis)
