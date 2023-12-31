from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")
    # 요청(request)에서 사용자 정보 가져오기
    user = request.user
    # 가져온 사용자의 로그인 여부 확인.
    is_authenticated = user.is_authenticated

    print("user : ", user)
    print("is_authenticated : ", is_authenticated)
    return render(request, 'posts/feeds.html')