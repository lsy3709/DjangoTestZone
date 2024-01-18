from django.urls import path
from users.views import login_view, logout_view, signup, profile

#추가
app_name = 'users'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('<int:user_id>/profile/', profile, name='profile'),

]