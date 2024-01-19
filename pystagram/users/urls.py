from django.urls import path
from users.views import login_view, logout_view, signup, profile, followers, following, follow, profile_edit, user_edit, update_password

#추가
app_name = 'users'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('user_edit/', user_edit, name='user_edit'),
    path('<int:user_id>/update_password/', update_password, name='update_password'),
    path('<int:user_id>/profile/', profile, name='profile'),
    path('<int:user_id>/profile/edit/', profile_edit, name='profile_edit'),
    path('<int:user_id>/followers/', followers, name='followers'),
    path('<int:user_id>/following/', following, name='following'),
    path('<int:user_id>/follow/', follow, name='follow'),


]