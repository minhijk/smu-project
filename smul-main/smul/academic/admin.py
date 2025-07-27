from django.contrib import admin
from .models import StudentProfile, LeaveRequest

# Register your models here.

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'name', 'gender', 'department', 'nationality',
        'phone', 'email', 'professor', 'eng_name',
        'bank', 'account_number', 'account_holder',
    )

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'status', 'submitted_at')