from django.urls import path
# 추가
from posts.views import feeds, comment_add, comment_delete, post_add

urlpatterns = [
    path('feeds/', feeds),
    #추가
    path('comment_add/', comment_add),
#추가
    path('comment_delete/<int:comment_id>/', comment_delete),
#추가
    path('post_add/',post_add),
]