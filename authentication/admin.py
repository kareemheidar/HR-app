from django.contrib import admin
from .models import cands

# Register your models here.
@admin.register(cands)
class CandidateAdmin(admin.ModelAdmin):
    pass
