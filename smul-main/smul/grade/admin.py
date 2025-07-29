from django.contrib import admin
from .models import TotalGrade

@admin.register(TotalGrade)
class TotalGradeAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'year', 'semester', 'total_credit', 'grade_point', 'grade_average', 'percentile', 'rank')
    search_fields = ('student_id', 'year', 'semester')
