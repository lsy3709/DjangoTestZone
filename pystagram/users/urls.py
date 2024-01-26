from django.contrib.auth.views import PasswordResetView
from django.urls import path

from users.views import login_view, logout_view, signup, profile, followers, following, follow, profile_edit, user_edit, \
    update_password, delete_user, reset_password, send_email, forgot_id, verify_code, auth_email

# 추가
app_name = 'users'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('forgot_id/', forgot_id, name='forgot_id'),
    path('auth_email/', auth_email, name='auth_email'),
    path('verify_code/', verify_code, name='verify_code'),
    path('user_edit/', user_edit, name='user_edit'),
    path('send_email/', send_email, name='send_email'),
    path('<int:user_id>/update_password/', update_password, name='update_password'),
    # path('<int:user_id>/reset_password/', reset_password, name='reset_password'),
    path('<int:user_id>/delete_user/', delete_user, name='delete_user'),
    path('<int:user_id>/profile/', profile, name='profile'),
    path('<int:user_id>/profile/edit/', profile_edit, name='profile_edit'),
    path('<int:user_id>/followers/', followers, name='followers'),
    path('<int:user_id>/following/', following, name='following'),
    path('<int:user_id>/follow/', follow, name='follow'),

]
