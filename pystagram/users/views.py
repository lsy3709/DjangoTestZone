# 추가
import random

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse

# 추가
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# 추가
from django.shortcuts import render, redirect, get_object_or_404

from posts.models import Post
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# 추가
from users.forms import LoginForm, SignupForm, CustomUserChangeForm, CustomPasswordResetForm
from users.models import User
from django.http import JsonResponse



# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        # 수정
        return redirect("posts:feeds")

    # 수정
    if request.method == "POST":
        # 인증 코드 6자리 가져와서, 세션과 일치 여부 확인 후 로그인 처리하기.
        form = LoginForm(data=request.POST)
        # 추가
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # 수정
                # 로그인 시도 횟수 초기화
                user.login_attempts = 0
                user.save()
                return redirect("posts:feeds")
            else:
                # print("로그인에 실패했습니다.")
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")

        context = {
            "form": form,
        }
        return render(request, 'users/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    # 수정
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
    posts = Post.objects.filter(user=user).order_by('-created')
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
        "login_user": login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }
    return render(request, 'users/profile.html', context)


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
    return render(request, 'users/profile.html', context)


def profile_edit(request, user_id):
    form = CustomUserChangeForm(instance=request.user)
    user = get_object_or_404(User, id=user_id)
    login_user = request.user
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
        "login_user": login_user,
        "form": form
    }
    return render(request, 'users/profile_edit.html', context)


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
        "form": form
    }
    return render(request, 'users/profile_edit_password.html', context)


def delete_user(request, user_id):
    request.user.delete()
    logout(request)
    return redirect("users:login")


def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    login_user = request.user
    context = {
        "user": user,
        "relationships": relationships,
        "login_user": login_user,
    }
    return render(request, 'users/followers.html', context)


def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    login_user = request.user
    context = {
        "user": user,
        "relationships": relationships,
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





def forgot_id(request):

    if request.method == 'POST':
        email = request.POST.get('find_email')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                context = {
                    'id' : user.username
                }
                template = render_to_string('users/email_findid_template_plain.html', context)
                #이메일에 아이디 표시 하는 방법.
                # send_email("Your ID is in the email", email, message)
                # 이메일에 링크 넣기
                send_email("Your ID is in the email", email, template)

                # return render(request, 'users/email_findid_template.html', context)
                return render(request, 'users/email_findid_template_test.html', context)
        except:
            messages.info(request, "해당 이메일로 등록된 사용자 ID가 존재하지않습니다.")
    context = {}
    return render(request, 'users/forgot_id.html', context)


def verify_code(request):
    # 추가
    if request.method == "POST":
        user_code = request.POST.get('input_code')
        stored_code = request.session.get('verification_code')

        if user_code == stored_code:
            # 인증 성공 후 세션 제거
            if 'verification_code' in request.session:
                del request.session['verification_code']
            # 인증 성공 시, 이동할 페이지 설정
            return redirect('users:forgot_id')

        else:
            # 인증 실패 시, 에러 메세지와 다시 로그인 페이지로 리다이렉트
            return redirect('users:login')  # 실패 시 로그인 페이지로 이동

    return render(request, 'users/verify_code.html')


def auth_email(request):
    return render(request, 'users/auth_email.html')

# def send_email(request):
#     subject = "message"
#     to = ["lsy3709@naver.com"]
#     from_email = "lsy3709@gmail.com"
#     message = "메지시 테스트, https://sylovestp.com"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
def send_email(subject, to,message):
    subject_send = subject
    to_send = []
    to_send.append(to)
    from_email = "lsy3709@gmail.com"
    message_send = message
    # 프로덕션 환경에서는 : fail_silently=Trun 로 진행
    EmailMessage(subject=subject_send, body=message_send, to=to_send, from_email=from_email).send(fail_silently=False)

def send_email_with_code(request):
    if request.method == 'POST':
        email = request.POST.get('verify_email')
        # 임시 세션에 6자리 랜덤 숫자 저장
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        request.session['verification_code'] = code
        request.session.set_expiry(300)  # 5분 (300초) 후 세션 만료
        message = f"인증코드: [{code}]"
        send_email("인증코드", email, message)
        # 성공 시
        # return redirect("users:verify_code")  # 인증 코드 확인 페이지로 이동

        return render(request, 'users/verify_code.html')

# rest 용 이메일 인증
class SendEmailWithCode(APIView):
    def post(self, request, format=None):
        email = request.data.get('verify_email')
        print(f"요청이 왔어 확인: {email}")

        if not email:
            return Response({'error': '이메일 주소를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 임시 세션에 6자리 랜덤 숫자 저장
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        request.session['verification_code_'+email] = code
        request.session.set_expiry(180)  # 3분 (180초) 후 세션 만료
        message = f"인증코드: [{code}]"
        send_email("인증코드", email, message)
        print(f"요청이 왔어 확인: {email}")

        # 성공 시, JSON 응답 반환
        return Response({'message': '이메일 전송이 완료되었습니다.!!'}, status=status.HTTP_200_OK)

    # rest 용 6자리 코드 인증
    class VerifyCode(APIView):
        def post(self, request, format=None):
            input_code = request.data.get('input_code')
            stored_code = request.session.get('verification_code_')
            print(f"코드 확인 요청이 왔어 input_code 확인: {input_code}")

            if not input_code:
                return Response({'error': '6자리 코드를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

            # 임시 세션에 6자리 랜덤 숫자 저장
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            request.session['verification_code'] = code
            request.session.set_expiry(180)  # 3분 (180초) 후 세션 만료
            message = f"인증코드: [{code}]"
            send_email("인증코드", email, message)
            print(f"요청이 왔어 확인: {email}")

            # 성공 시, JSON 응답 반환
            return Response({'message': '이메일 전송이 완료되었습니다.!!'}, status=status.HTTP_200_OK)


