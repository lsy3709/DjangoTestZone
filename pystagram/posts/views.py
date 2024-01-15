from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
#추가
from posts.forms import CommentForm, PostForm
#추가
from posts.models import Post, Comment, PostImage

#추가
from django.views.decorators.http import require_POST

#추가
from django.http import HttpResponseRedirect, HttpResponseForbidden

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")


    # 요청(request)에서 사용자 정보 가져오기
    #user = request.user
    # 가져온 사용자의 로그인 여부 확인.
    #is_authenticated = user.is_authenticated

    #print("user : ", user)
    #print("is_authenticated : ", is_authenticated)

    #추가
    posts = Post.objects.all()
    # 추가
    comment_form = CommentForm()

    context = {
        "posts": posts,
        # 추가
        "comment_form": comment_form,
    }
    return render(request, 'posts/feeds.html',context)

@require_POST
def comment_add(reqeust):
    form = CommentForm(data=reqeust.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = reqeust.user
        comment.save()

        print(comment.id)
        print(comment.content)
        print(comment.user)
        # 수정
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    else:
        return HttpResponseForbidden("댓글 삭제 권한이 없습니다.")

def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )
            url = f"/posts/feeds/#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()

    context = {
        "form" : form
    }
    return render(request, 'posts/post_add.html',context)

