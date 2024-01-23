from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
#추가
from posts.forms import CommentForm, PostForm, PostImageForm
#추가
from posts.models import Post, Comment, PostImage, HashTag

#추가
from django.views.decorators.http import require_POST

#추가
from django.http import HttpResponseRedirect, HttpResponseForbidden

#추가
from django.urls import reverse

#추가
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        #수정
        return redirect("users:login")


    # 요청(request)에서 사용자 정보 가져오기
    #user = request.user
    # 가져온 사용자의 로그인 여부 확인.
    #is_authenticated = user.is_authenticated

    #print("user : ", user)
    #print("is_authenticated : ", is_authenticated)

    #추가 , 포스트 글 생성일로 최신순 변경
    posts = Post.objects.all().order_by('-created')
    # 추가
    comment_form = CommentForm()

    page = request.GET.get('page')
    paginator = Paginator(posts,2)


    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

#추가
    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex + 1)

    context = {
        "posts": posts,
        # 추가
        "comment_form": comment_form,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range":custom_range
    }
    return render(request, 'posts/feeds.html',context)

@require_POST
def comment_add(reqeust):
    form = CommentForm(data=reqeust.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = reqeust.user
        comment.save()

        #추가
        if reqeust.GET.get("next"):
            url_next = reqeust.GET.get("next")
        else:
            url_next = reverse("posts:feeds") + f"#post-{comment.post.id}"

        return HttpResponseRedirect(url_next)


@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        # 수정
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
        # return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    else:
        return HttpResponseForbidden("댓글 삭제 권한이 없습니다.")

@require_POST
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        # 수정
        url = reverse("posts:feeds")
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("게시글 삭제 권한이 없습니다.")



def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        if post.user == request.user:
            post_form = PostForm(request.POST, instance=post)
            # image_form = PostImageForm(request.POST, request.FILES)
            # if post_form.is_valid() and image_form.is_valid():
            if post_form.is_valid():
                post_form.save()
                # image_instance = image_form.save(commit=False)
                # image_instance.post = post
                # image_instance.save()
            # 수정
            url = reverse("posts:feeds")
            return HttpResponseRedirect(url)

    else:
        form = PostForm()
    context = {
        "post": post,
    }
    return render(request, 'posts/post_edit.html', context)

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
            #추가
            tag_string = request.POST.get("tags")
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
                for tag_name in tag_names:
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

                #수정
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()

    context = {
        "form" : form
    }
    return render(request, 'posts/post_add.html',context)


#추가
def tags(request, tag_name):
    # 추가
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    # 추가
    else:
        posts = Post.objects.filter(tags = tag)
    context = {
        "tag_name" : tag_name,
        "posts" : posts,
    }

    return render(request, 'posts/tags.html', context)

#추가
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    # 추가
    comment_form = CommentForm()
    context = {"post" : post ,
               "comment_form" : comment_form,}
    return render(request, 'posts/post_detail.html', context)

#추가
def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user.like_posts.filter(id=post.id).exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)
    url_next = request.GET.get("next") or reverse("posts:feeds")+f"#post-{post.id}"
    return HttpResponseRedirect(url_next)

