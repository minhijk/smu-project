from django.contrib import admin
from .models import GraduationRequirement

@admin.register(GraduationRequirement)
class GraduationRequirementAdmin(admin.ModelAdmin):
    list_display = [
        'college', 'department', 'entry_type',
        'lib_req', 'lib_sel', 'lib_total',
        'major_core', 'major_sel', 'major_total',
        'double_req', 'double_sel', 'double_total',
        'sub_major1', 'sub_major2',
        'remain_credit', 'grad_avg', 'gpa_grad', 'gpa_early'
    ]
