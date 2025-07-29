from django.db import models

class GraduationRequirement(models.Model):
    # 🔹 소속 정보
    college = models.CharField(max_length=100)       # 예: 융복합특성화대
    department = models.CharField(max_length=100)    # 예: 만화전공
    entry_type = models.CharField(max_length=20)     # 입학구분 (예: 일반, 편입 등)

    # 🔹 교양
    lib_req = models.IntegerField()      # 교양 필수
    lib_sel = models.IntegerField()      # 교양 선택
    lib_total = models.IntegerField()    # 교양 계

    # 🔹 전공(단일전공 기준)
    major_core = models.IntegerField(blank=True, null=True)   # 전공 심화 (전심)
    major_sel = models.IntegerField()    # 전공 선택 (전선)
    major_total = models.IntegerField()  # 전공 계

    # 🔹 전공(다전공)
    double_req = models.IntegerField()   # 전공 필수
    double_sel = models.IntegerField()   # 전공 선택
    double_total = models.IntegerField() # 계

    # 🔹 부전공
    sub_major1 = models.IntegerField(blank=True, null=True)   # 1전공
    sub_major2 = models.IntegerField()   # 부전공

    # 🔹 기타
    remain_credit = models.IntegerField()   # 잔여학점
    grad_avg = models.FloatField()          # 졸업 이수 기준
    gpa_grad = models.FloatField()          # 졸업 평점 평균
    gpa_early = models.FloatField(blank=True, null=True)         # 조기졸업 평점 평균

    def __str__(self):
        return f"{self.college} {self.department}"
