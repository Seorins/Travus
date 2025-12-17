from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """사용자 모델"""
    DISABILITY_CHOICES = [
        ('NONE', '없음'),
        ('PHYSICAL', '지체장애'),
        ('VISUAL', '시각장애'),
        ('HEARING', '청각장애'),
        ('ELDERLY', '고령자'),
        ('INFANT', '영유아동반'),
        ('OTHER', '기타'),
    ]

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='전화번호')
    disability_type = models.CharField(
        max_length=20,
        choices=DISABILITY_CHOICES,
        default='NONE',
        verbose_name='장애 유형'
    )
    preferred_accessibility = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='선호 접근성 옵션'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return self.username
