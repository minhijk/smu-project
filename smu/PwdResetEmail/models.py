from django.db import models
from django.utils import timezone

class EmailAuthCode(models.Model):
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)  # 이메일 인증이 아니면 빈칸
    phone = models.CharField(max_length=20, null=True, blank=True)  # ✅ 추가
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def is_re_request_blocked(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=1)
