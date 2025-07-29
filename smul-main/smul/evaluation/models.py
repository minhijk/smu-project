# evaluation/models.py
from django.db import models

class EvalResult(models.Model):
    student_id = models.CharField(max_length=20)
    course_code = models.CharField(max_length=20)
    eval_type = models.CharField(max_length=10, choices=(('mid', '중간'), ('final', '기말')))
    score = models.IntegerField()
    comment = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.course_code} ({self.eval_type})"
