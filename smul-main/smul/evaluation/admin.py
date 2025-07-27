from django.contrib import admin
from .models import EvalResult


@admin.register(EvalResult)
class EvalResultAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'course_code', 'eval_type', 'score', 'submitted_at')
    list_filter = ('eval_type', 'submitted_at')
    search_fields = ('student_id', 'course_code', 'comment')
    ordering = ('-submitted_at',)
