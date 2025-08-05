from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, student_id, password=None, **extra_fields):
        if not student_id:
            raise ValueError('학번은 필수입니다.')
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(student_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', '관리자'),
        ('professor', '교수'),
        ('student', '학생'),
    ]
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # ✅ 역할이 'admin'이면 관리자 권한 자동 부여
        if self.role == 'admin':
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student_id
    

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

