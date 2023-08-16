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

