from django.urls import path
# 추가
from posts.views import feeds, comment_add, comment_delete, post_add, tags, post_detail, post_like, post_delete, \
    post_edit, post_image_delete, post_tag_delete, post_search

# 추가
app_name = 'posts'
urlpatterns = [
    path('feeds/', feeds, name="feeds"),
    # 추가
    path('comment_add/', comment_add, name="comment_add"),
    # 추가
    path('comment_delete/<int:comment_id>/', comment_delete, name="comment_delete"),
    # 추가
    path('post_add/', post_add, name="post_add"),
    # 추가
    path('post_search/', post_search, name="post_search"),
    # 추가,
    path('post_edit/<int:post_id>/', post_edit, name='post_edit'),
    # 추가
    path('post_delete/<int:post_id>/', post_delete, name="post_delete"),
    # 추가
    path('post_image_delete/<int:post_id>/<int:image_id>/', post_image_delete, name="post_image_delete"),
    # 추가
    path('post_tag_delete/<int:post_id>/<int:tag_id>/', post_tag_delete, name="post_tag_delete"),
    # 추가
    path('tags/<str:tag_name>/', tags, name="tags"),
    # 추가
    path('<int:post_id>/', post_detail, name="post_detail"),
    # 추가
    path('<int:post_id>/like/', post_like, name="post_like"),
]
