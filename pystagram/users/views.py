#추가
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse

#추가
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
#추가
from django.shortcuts import render, redirect, get_object_or_404
#추가
from users.forms import LoginForm, SignupForm, CustomUserChangeForm
from users.models import User


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        # 수정
        return redirect("posts:feeds")

    #수정
    if request.method == "POST":

        form = LoginForm(data=request.POST)
        #추가
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user :
                login(request, user)
                #수정
                return redirect("posts:feeds")
            else:
                # print("로그인에 실패했습니다.")
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")


        context = {
            "form": form ,
        }
        return render(request, 'users/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form" : form
        }
        return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    #수정
    return redirect("users:login")

def signup(request):
    # 추가
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # 수정
            return redirect("posts:feeds")

    else:
        form = SignupForm()

    context = {"form": form}
    return render(request, 'users/signup.html', context)




def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    login_user = request.user
    print("user", user)
    print("login_user", login_user)
    print("request.user.is_authenticated",request.user.is_authenticated)
    context = {
        "user": user,
        "login_user":login_user
    }
    return render(request, 'users/profile.html',context)

def user_edit(request):
    # 추가
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            # 수정
            return redirect("posts:feeds")

    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {"form": form,
               }
    return render(request, 'users/profile.html',context)
def profile_edit(request, user_id):
    form = CustomUserChangeForm(instance=request.user)
    user = get_object_or_404(User, id=user_id)
    login_user = request.user
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
        "login_user": login_user,
        "form" :form
    }
    return render(request, 'users/profile_edit.html',context)

def update_password(request, user_id):
    if request.method == "GET":
        form = PasswordChangeForm(request.user)

    else:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("posts:feeds")

    user = get_object_or_404(User, id=user_id)
    login_user = request.user
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
        "login_user": login_user,
        "form" :form
    }
    return render(request, 'users/profile_edit_password.html',context)

def delete_user(request,user_id):
     request.user.delete()
     logout(request)
     return redirect("users:login")



def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    login_user = request.user
    context = {
        "user" : user,
        "relationships" : relationships,
        "login_user": login_user,
    }
    return render(request, 'users/followers.html', context)


def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    login_user = request.user
    context = {
        "user" : user,
        "relationships" : relationships,
        "login_user": login_user,
    }
    return render(request, 'users/following.html', context)


def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if target_user in user.following.all():
        user.following.remove(target_user)
    else:
        user.following.add(target_user)
    url_next = request.GET.get('next') or reverse('users:profile', args=[user.id])
    return HttpResponseRedirect(url_next)




