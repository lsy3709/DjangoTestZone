#추가
import random

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse

#추가
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
#추가
from django.shortcuts import render, redirect, get_object_or_404

from posts.models import Post
#추가
from users.forms import LoginForm, SignupForm, CustomUserChangeForm, CustomPasswordResetForm
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
                # 로그인 시도 횟수 초기화
                user.login_attempts = 0
                user.save()
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
    posts = Post.objects.filter(user = user).order_by('-created')
    # print("user", user)
    # print("login_user", login_user)
    # print("request.user.is_authenticated",request.user.is_authenticated)
    # print("posts",posts)
    page = request.GET.get('page')
    paginator = Paginator(posts, 18)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex + 1)

    context = {
        "user": user,
        "login_user":login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
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

def reset_password(request, user_id):
    if request.method == "GET":
        form = CustomPasswordResetForm()

    else:
        user = get_object_or_404(User, id=user_id)
        form = CustomPasswordResetForm()
        if form.is_valid():
            form.save()
            return redirect("posts:feeds")

    user = get_object_or_404(User, id=user_id)
    login_user = request.user
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
        "login_user": login_user,
        "form": form
    }
    return render(request, 'users/profile_edit_reset_password.html', context)

def send_email(request):
    subject = "message"
    to = ["lsy3709@naver.com"]
    from_email = "lsy3709@gmail.com"
    message = "메지시 테스트, https://sylovestp.com"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

def forgot_id(request):
    if request.method == "GET":
        form = CustomPasswordResetForm()

    else:
        # user = get_object_or_404(User, id=user_id)
        form = CustomPasswordResetForm()
        # if form.is_valid():
        #     form.save()
        #     return redirect("posts:feeds")


    context = {
        "form": form
    }
    return render(request, 'users/forgot_id.html', context)

def verify_code(request):
    # 추가
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # 수정
            return redirect("posts:feeds")

    return render(request, 'users/verify_code.html')

def auth_email(request):
    return render(request, 'users/auth_email.html')


def send_email_with_code(request):
    if request.method == 'POST':
        email = request.POST.get('verify_email')
        # 임시 세션에 6자리 랜덤 숫자 저장
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        request.session['verification_code'] = code
        subject = "인증코드"
        to = []
        to.append(email)
        from_email = "lsy3709@gmail.com"
        message = f"인증코드: [{code}]"
        print(f"code : {code}, email : {email}, subject : {subject}, to : {to}, from : {from_email}, message : {message}")
        email_message = EmailMessage(
        subject=subject,
        body=message,
        to=to,
        from_email=from_email
          )
        email_message.send()
        # 성공 시
        return redirect("users:verify_code")  # 인증 코드 확인 페이지로 이동