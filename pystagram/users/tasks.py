# tasks.py

from django.core.management.base import BaseCommand
from users.models import VerificationCode  # 특정 모델을 가져와야 합니다.

def delete_records():
    # 이 함수에서는 특정 조건을 사용하여 레코드를 삭제합니다.
    # 예를 들어, 여기서는 30일 이상된 레코드를 삭제합니다.
    # VerificationCode.objects.filter(created_at__lte=timezone.now() - timedelta(days=30)).delete()
    VerificationCode.objects.objects.all().delete()

