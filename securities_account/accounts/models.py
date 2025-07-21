from django.contrib.auth.models import User
from django.db import models


class AccountApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '審核中'),
        ('APPROVED', '已通過'),
        ('REJECTED', '已拒絕'),
        ('ADDITIONAL', '待補件'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 補件與拒絕用欄位
    rejection_reason = models.TextField(blank=True, null=True)
    additional_requirements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_name}"
