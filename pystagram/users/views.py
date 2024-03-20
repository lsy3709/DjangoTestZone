# 추가
import random

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

# 추가
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# 추가
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from posts.models import Post, Message
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# 추가
from users.forms import LoginForm, SignupForm, CustomUserChangeForm, CustomPasswordResetForm
from users.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from users.models import VerificationCode
import json
import logging

logger = logging.getLogger('pystagram')





# rest 용 6자리 코드 인증
class session_timeout(APIView):
    def session_timeout(self, request, format=None):
        expiration = request.session.get_expiry_date()

        remaining_seconds = (expiration - timezone.now()).total_seconds()

        return Response({'timeout': remaining_seconds}, status=status.HTTP_200_OK)


@require_POST
def extend_session(request):
    """
    세션 타임아웃을 연장합니다.
    """
    request.session.set_expiry(300)  # 다시 5분 추가
    return JsonResponse({'status': 'Session extended'})


# Create your views here.
def login_view(request):
    # logger.info("info 레벨 출력 확인")
    if request.user.is_authenticated:
        # 수정
        return redirect("posts:feeds")

    # 수정
    if request.method == "POST":
        # 인증 코드 6자리 가져와서, 세션과 일치 여부 확인 후 로그인 처리하기.
        form = LoginForm(data=request.POST)
        verify_email = request.POST.get('email-input')
        input_code = request.POST.get('input_code')

        # 추가
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user:

                try:
                    verification_code = VerificationCode.objects.get(user_email=verify_email, code=input_code)
                    login(request, user)
                    # 수정
                    # 로그인 시도 횟수 초기화
                    user.login_attempts = 0
                    verification_code.delete()
                    user.save()
                    return redirect("posts:feeds")
                except:
                    form.add_error(None, "인증코드가 일치하지 않습니다..")
            else:
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
        verify_email = request.POST.get('email')
        input_code = request.POST.get('input_code')
        if form.is_valid():

            try:
                verification_code = VerificationCode.objects.get(user_email=verify_email, code=input_code)
                user = form.save()
                verification_code.delete()
                login(request, user)
                # 수정
                return redirect("posts:feeds")
            except:
                form.add_error(None, "인증코드가 일치하지 않습니다..")

    else:
        form = SignupForm()

    context = {"form": form}
    return render(request, 'users/signup.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(receiver=user).order_by('-created')
    login_user = request.user
    posts = Post.objects.filter(user=user).order_by('-created')
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
        "messages": messages,
        "login_user": login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }
    return render(request, 'users/profile.html', context)


# 프로필 수정폼, 처리
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


# 프로필 수정폼
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


# 패스워드 수정
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
    messages = Message.objects.filter(receiver=user).order_by('-created')
    relationships = user.follower_relationships.all()
    login_user = request.user
    # 페이징 추가
    page = request.GET.get('page')
    paginator = Paginator(relationships, 18)

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
        "relationships": relationships,
        "messages": messages,
        "login_user": login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }
    return render(request, 'users/followers.html', context)


def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(receiver=user).order_by('-created')
    relationships = user.following_relationships.all()
    login_user = request.user
    # 페이징 추가
    page = request.GET.get('page')
    paginator = Paginator(relationships, 18)

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
        "relationships": relationships,
        "messages": messages,
        "login_user": login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }
    return render(request, 'users/following.html', context)


def messageBox(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(receiver=user).order_by('-created')
    login_user = request.user
    # 페이징 추가
    page = request.GET.get('page')
    paginator = Paginator(messages, 5)

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
        "messages": messages,
        "login_user": login_user,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }
    return render(request, 'users/messageInbox.html', context)


def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if target_user in user.following.all():
        user.following.remove(target_user)
    else:
        user.following.add(target_user)
    url_next = request.GET.get('next') or reverse('users:profile', args=[user.id])
    return HttpResponseRedirect(url_next)


# 패스워드 초기화, 사용 안하고 있음.
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


# 아이디 찾기 
def forgot_id(request):
    if request.method == 'POST':
        email = request.POST.get('email-input')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                context = {
                    'id': user.username
                }
                template = render_to_string('users/email_findid_template_plain.html', context)
                # 이메일에 아이디 표시 하는 방법.
                # send_email("Your ID is in the email", email, message)
                # 이메일에 링크 넣기
                send_email("Your ID is in the email", email, template)

                # return render(request, 'users/email_findid_template.html', context)
                return redirect('users:login')
        except:
            messages.info(request, "해당 이메일로 등록된 사용자 ID가 존재하지않습니다.")
    context = {}
    return render(request, 'users/forgot_id.html', context)


# 6자리 코드 확인 , 세션으로 확인
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


# 테스트 메일 보내기
def send_email(subject, to, message):
    subject_send = subject
    to_send = []
    to_send.append(to)
    from_email = "lsy3709@gmail.com"
    message_send = message
    # 프로덕션 환경에서는 : fail_silently=Trun 로 진행
    EmailMessage(subject=subject_send, body=message_send, to=to_send, from_email=from_email).send(fail_silently=False)


# 테스트6자리 코드 , 메일 보내기, 세션 저장 버전
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


# rest 용 이메일 인증 , 6자리 코드, VerificationCode 테이블에 저장
class SendEmailWithCode(APIView):
    def post(self, request, format=None):
        email = request.data.get('verify_email')

        if not email:
            return Response({'error': '이메일 주소를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 임시 세션에 6자리 랜덤 숫자 저장
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        print(f"생성된 6자리 코드 : {code}")
        user_email = email
        if code:
            # 데이터를 DB에 저장
            verification_code = VerificationCode(code=code, user_email=user_email)
            verification_code.save()

        message = f"인증코드: [{code}]"
        send_email("인증코드", email, message)

        # 성공 시, JSON 응답 반환
        return Response({'message': '이메일 전송이 완료되었습니다.!!'}, status=status.HTTP_200_OK)


# 메세지 단수 또는 복수개 삭제 하는 기능, Rest 용
class DeleteMessage(APIView):
    def post(self, request, format=None):
        # 리스트로 넘어온 메세지 아이디를 , 리스트로 담기.
        # 반복문으로 해당 메세지 삭제.
        # 다시 메세지 박스로 복귀

        if request.method == "POST":

            # print("도착은 했니?")
            # JSON 데이터를 받음
            received_data = request.data
            # print("받은 데이터:", received_data)

            for data in received_data:
                # 특정 사용자에게 수신된 메시지 필터링
                message = Message.objects.get(id=data)

                # 메시지 삭제
                message.delete()

            return Response({"message": "데이터를 삭제했습니다."})


# rest 용 6자리 코드 인증
class VerifyCode(APIView):
    def post(self, request, format=None):
        verify_email = request.data.get('verify_email')
        input_code = request.data.get('verify_input_code')
        try:
            # DB에서 데이터를 가져와서 확인
            # verification_code = VerificationCode.objects.get(user_email=verify_email, code=input_code)

            # DB에서 데이터 삭제
            verification_code = VerificationCode.objects.get(user_email=verify_email, code=input_code)
            verification_code.delete()

            return Response({'message': '인증 확인 성공.'}, status=status.HTTP_200_OK)

        except VerificationCode.DoesNotExist:
            return Response({'error': '코드가 일치하지 않거나 DB에 없습니다..'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyCode_noDelete(APIView):
    def post(self, request, format=None):
        verify_email = request.data.get('verify_email')
        input_code = request.data.get('verify_input_code')
        try:
            verification_code = VerificationCode.objects.get(user_email=verify_email, code=input_code)
            return Response({'message': '인증 확인 성공2.'}, status=status.HTTP_200_OK)

        except VerificationCode.DoesNotExist:
            return Response({'error': '코드가 일치하지 않거나 DB에 없습니다..'}, status=status.HTTP_400_BAD_REQUEST)


# 404 페이지
def page_not_found(request, exception):
    return render(request, 'users/404.html', {})


# 500 페이지
def server_error_page(request):
    return render(request, 'users/500.html', {})
