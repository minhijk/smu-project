from django.db import models

# Create your models here.

class TotalGrade(models.Model):
    student_id = models.CharField(max_length=20)  # 학번
    year = models.CharField(max_length=10)        # 학년도 (예: "2023")
    semester = models.CharField(max_length=10)    # 학기 (예: "1학기" or "1")
    total_credit = models.IntegerField()          # 신청학점
    grade_point = models.FloatField()             # 평점계
    grade_average = models.FloatField()           # 평점평균
    percentile = models.FloatField()              # 백분율
    rank = models.CharField(max_length=20)        # 석차 (예: "1/35")

    def __str__(self):
        return f"{self.student_id} - {self.year} {self.semester}"
