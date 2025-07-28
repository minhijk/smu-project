# smul/academic/models.py
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    professor = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    account_holder = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    address_detail = models.CharField(max_length=200, blank=True, null=True)
    total_credit = models.PositiveIntegerField(default=0)     # 총 취득학점
    major_credit = models.PositiveIntegerField(default=0)     # 전공학점
    liberal_credit = models.PositiveIntegerField(default=0)   # 교양학점
    general_credit = models.PositiveIntegerField(default=0)   # 일반선택
    teaching_credit = models.PositiveIntegerField(default=0)  # 교직학점
    etc_credit = models.PositiveIntegerField(default=0)       # 기타학점
    gpa = models.FloatField(default=0.0)                      # 평균 평점

    def __str__(self):
        return f"{self.name} ({self.student_id})"


STATUS_CHOICES = [
    ('휴학', '휴학'),
    ('복학', '복학'),
    ('자퇴', '자퇴'),
]

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    document = models.FileField(upload_to='leave_documents/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
