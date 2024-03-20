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

    def save(self, *args, **kwargs):
        # 이미지를 열고 크기를 조절합니다.
        img = Image.open(self.profile_image)
        output = io.BytesIO()

        # 이미지의 크기를 확인하고 조절합니다. 여기서는 너비가 800px을 넘지 않도록 합니다.
        if img.width > 800:
            output_size = (800, (800 * img.height) // img.width)
            img = img.resize(output_size, Image.ANTIALIAS)

        # 변경된 이미지를 저장합니다.
        img.save(output, format='JPEG', quality=90)
        output.seek(0)

        # InMemoryUploadedFile을 사용하여 Django가 파일을 처리하도록 합니다.
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                          output.tell(), None)

        super().save(*args, **kwargs)

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