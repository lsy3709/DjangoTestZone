from django.core.exceptions import ValidationError
from django.db import models
import os

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
    )
    content = models.TextField("내용",max_length=2000)
    created = models.DateTimeField("생성일시", auto_now_add=True)
    #추가
    tags = models.ManyToManyField("posts.HashTag", verbose_name="해시태그 목록", blank=True)
    #추가
    def __str__(self):
        return f"{self.user.username}의 Post(id:{self.id})"

    def save(self, *args, **kwargs):
        # content 필드의 길이가 2000자를 초과할 경우 ValidationError을 발생시킵니다.
        if len(self.content) > 2000:
            raise ValidationError("글 내용은 2000자를 초과할 수 없습니다.")
        super().save(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="포스트",
        on_delete=models.CASCADE,
    )
    photo = models.ImageField("사진", upload_to="post")

    def clean(self):
        # 이미지 장수를 제한하는 로직을 clean 메서드에 구현합니다.
        max_images = 10  # 허용하는 최대 이미지 장수
        current_images = PostImage.objects.filter(post=self.post).count()
        if current_images >= max_images:
            raise ValidationError(f"이미지는 최대 {max_images}장까지 업로드할 수 있습니다.")

    def save(self, *args, **kwargs):
        self.full_clean()  # clean 메서드를 호출하여 유효성 검사를 수행합니다.
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, verbose_name="포스트", on_delete=models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("생성일시", auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(
        "users.User",
        verbose_name="보낸사람",
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        "Post",
        verbose_name="받는사람",
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField("내용")
    created = models.DateTimeField("생성일시", auto_now_add=True)

class HashTag(models.Model):
    name = models.CharField("태그명", max_length=50)

    def __str__(self):
        return self.name


