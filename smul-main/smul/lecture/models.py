from django.db import models

class userLecture(models.Model):
    student_id = models.CharField(max_length=20)  # 학번
    course_code = models.CharField(max_length=20)  # 학수번호
    course_name = models.CharField(max_length=100)  # 교과목명
    credit = models.IntegerField()  # 학점
    semester = models.CharField(max_length=10)  # 예: '2025-2'
    day_time = models.CharField(max_length=50)  # 예: '화1,2,3'
    professor = models.CharField(max_length=50)  # 담당교수
