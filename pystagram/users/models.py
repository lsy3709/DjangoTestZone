import io

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일 필
    profile_image = models.ImageField(
        "프로필 이미지",upload_to='users/profile', blank=True)
    short_description = models.TextField("소개글",blank=True)
    #좋아요
    like_posts = models.ManyToManyField(
        "posts.Post",
        verbose_name="좋아요 누른 Post 목록",
        related_name="like_users",
        blank=True,
    )

    # # 메세지함
    # message_box = models.ManyToManyField(
    #     "posts.Message",
    #     verbose_name="전달받은 메세지 목록",
    #     related_name="message_inbox",
    #     blank=True,
    # )
    # 팔로잉
    following = models.ManyToManyField(
        "self",
        verbose_name="팔로우 중인 사용자들",
        related_name="followers",
        symmetrical=False,
        through="users.Relationship",
    )
    #로그인 횟수 컬럼
    login_attempts = models.PositiveIntegerField(default=0)
    #추가
    def __str__(self):
        return self.username



class Relationship(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우를 요청한 사용자",
        related_name="following_relationships",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 요청의 대상",
        related_name="follower_relationships",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"관계 ({self.from_user} -> {self.to_user})"

class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user_email = models.EmailField()
    created_at = models.DateTimeField()
    def save(self, *args, **kwargs):
        # 등록된 시간 필드가 None 또는 다른 시간과 다른 경우에만 현재 시간으로 설정
        if not self.created_at or self.created_at != timezone.now():
            self.created_at = timezone.now()
        super().save(*args, **kwargs)