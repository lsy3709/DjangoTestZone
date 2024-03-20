from django.contrib.auth.views import PasswordResetView
from django.urls import path

from users.views import login_view, logout_view, signup, profile, followers, following, follow, profile_edit, user_edit, \
    update_password, delete_user, reset_password, send_email, forgot_id, verify_code, send_email_with_code, \
    SendEmailWithCode, VerifyCode, VerifyCode_noDelete, messageBox, DeleteMessage, session_timeout, extend_session

# 추가
app_name = 'users'
urlpatterns = [
    path('session_timeout/', session_timeout.as_view(), name='session_timeout'),
    path('extend_session/', extend_session, name='extend_session'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('forgot_id/', forgot_id, name='forgot_id'),
    path('send_email_with_code/', send_email_with_code, name='send_email_with_code'),
    path('send_email_with_code_rest/', SendEmailWithCode.as_view(), name='send_email_with_code'),
    path('delete_message_rest/', DeleteMessage.as_view(), name='delete_message_rest'),

    path('verify_code_rest/', VerifyCode.as_view(), name='verify_code_rest'),
    path('verify_code_rest_noDelete/', VerifyCode_noDelete.as_view(), name='verify_code_rest_noDelete'),
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
    path('<int:user_id>/messageBox/', messageBox, name='messageBox'),
    path('<int:user_id>/follow/', follow, name='follow'),

]
