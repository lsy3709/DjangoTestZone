from django.contrib import admin

from posts.forms import PostForm
# 추가
from posts.models import Post, PostImage, Comment, HashTag
# 추가
# from django.contrib.admin.widgets import AdminFileWidget
# from django.db import models
# from django.utils.safestring import mark_safe

# 방법2
import admin_thumbnails

#추가
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple


# Register your models here.

# 추가
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1



# 추가
# class  InlineImageWidget(AdminFileWidget):
#     def render(self, name, value, attrs=None, renderer=None):
#         html = super().render(name,value, attrs, renderer)
#         if value and getattr(value, "url", None):
#             html = mark_safe(f'<img src="{value.url}" height="150">') + html
#         return  html
#

#방법2
# 추가
@admin_thumbnails.thumbnail('photo')
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    #방법1
    # formfield_overrides = {
    #     models.ImageField: {
    #         'widget': InlineImageWidget,
    #     }
    # }

#추가
class LikeUserInline(admin.TabularInline):
    model = Post.like_users.through
    verbose_name = '좋아요 한 User'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
    ]
    inlines = [
        CommentInline,
        PostImageInline,
    #추가
        LikeUserInline,

    ]

    #추가
    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "photo",
    ]




@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass

