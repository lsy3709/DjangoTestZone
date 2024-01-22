from django.urls import path
# 추가
from posts.views import feeds, comment_add, comment_delete, post_add, tags, post_detail, post_like, feed_delete

# 추가
app_name = 'posts'
urlpatterns = [
    path('feeds/', feeds, name="feeds"),
#추가
    path('feed_delete/<int:feed_id>/', feed_delete, name="feed_delete"),
    #추가
    path('comment_add/', comment_add, name="comment_add"),
#추가
    path('comment_delete/<int:comment_id>/', comment_delete, name="comment_delete"),
#추가
    path('post_add/',post_add, name="post_add"),
#추가
    path('tags/<str:tag_name>/', tags, name="tags"),
#추가
    path('<int:post_id>/', post_detail, name="post_detail"),
#추가
    path('<int:post_id>/like/', post_like, name="post_like"),
]