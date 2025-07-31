from django.contrib.auth.models import User
from django.db import models

class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('seoul', '서울'),
        ('cheonan', '천안'),
        ('employment', '채용'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AcademicEvent(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title