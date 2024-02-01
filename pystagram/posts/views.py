import os
import zipfile
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# 추가
from posts.forms import CommentForm, PostForm, PostImageForm
# 추가
from posts.models import Post, Comment, PostImage, HashTag

# 추가
from django.views.decorators.http import require_POST

# 추가
from django.http import HttpResponseRedirect, HttpResponseForbidden

# 추가
from django.urls import reverse

# 추가
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from users.models import User

from PIL import Image


# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        # 수정
        return redirect("users:login")

    # 요청(request)에서 사용자 정보 가져오기
    # user = request.user
    # 가져온 사용자의 로그인 여부 확인.
    # is_authenticated = user.is_authenticated

    # 추가 , 포스트 글 생성일로 최신순 변경
    posts = Post.objects.all().order_by('-created')
    # 추가
    comment_form = CommentForm()

    page = request.GET.get('page')
    paginator = Paginator(posts, 3)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    # 추가
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
        "custom_range": custom_range
    }
    return render(request, 'posts/feeds.html', context)


@require_POST
def comment_add(reqeust):
    form = CommentForm(data=reqeust.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = reqeust.user
        comment.save()

        # 추가
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


@require_POST
def post_image_delete(request, post_id, image_id):
    post = Post.objects.get(id=post_id)
    post_image = PostImage.objects.get(id=image_id)
    if post.user == request.user:
        post_image.delete()
        # 수정
        url = reverse("posts:post_edit", kwargs={"post_id": post_id})
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("이미지 삭제 권한이 없습니다.")


@require_POST
def post_tag_delete(request, post_id, tag_id):
    post = Post.objects.get(id=post_id)
    hastag = HashTag.objects.get(id=tag_id)
    if post.user == request.user:
        post.tags.remove(hastag)
        # 수정
        url = reverse("posts:post_edit", kwargs={"post_id": post_id})
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("태그 삭제 권한이 없습니다.")


def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        if post.user == request.user:
            post_form = PostForm(request.POST, instance=post)
            # image_form = PostImageForm(request.POST, request.FILES)
            # if post_form.is_valid() and image_form.is_valid():
            if post_form.is_valid():
                post_form.save()

            if request.FILES.getlist("images"):
                for image_file in request.FILES.getlist("images"):
                    PostImage.objects.create(
                        post=post,
                        photo=image_file,
                    )

            if request.POST.get("tags"):
                tag_string = request.POST.get("tags")
                if tag_string:
                    tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
                    for tag_name in tag_names:
                        tag, _ = HashTag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag)
            # 수정
            url = reverse("posts:feeds")
            return HttpResponseRedirect(url)

    else:
        form = PostForm()
    context = {
        "post": post,
    }
    return render(request, 'posts/post_edit.html', context)


def post_search(request):
    context = {
    }
    return render(request, 'posts/post_search.html', context)


def post_search_do(request):
    if request.method == "POST" :
        # 수정
        searchDB = request.POST.get('searchDB')
        content = request.POST.get('content')

    elif request.method == "GET":
            # 수정
        searchDB = request.GET.get('searchDB')
        content = request.GET.get('content')

    if content :
        if searchDB == "content":
            posts = Post.objects.filter(content__icontains=content).order_by('-created')
        elif searchDB == "tag":
            posts = Post.objects.filter(tags__name__icontains=content).order_by('-created')
        elif searchDB == "user":
            users = User.objects.filter(username__icontains=content)
            posts = Post.objects.filter(user__in=users).order_by('-created')

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
        "posts": posts,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range,
        "searchDB" : searchDB,
        "content" : content
    }
    return render(request, 'posts/post_search_result.html', context)


def post_download_images(request, post_id):
    # 게시글 객체 가져오기
    post = get_object_or_404(Post, pk=post_id)
    images = PostImage.objects.filter(post=post)

    # 이미지 파일들을 임시 디렉터리에 저장
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    zip_filename = f"images_for_post_{post_id}.zip"
    zip_file_path = os.path.join(temp_dir, zip_filename)

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image in images:
            image_path = image.photo.path
            zipf.write(image_path, os.path.basename(image_path))

    # 압축된 파일을 응답으로 전송
    with open(zip_file_path, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # 임시 디렉터리와 파일 삭제
    os.remove(zip_file_path)
    os.rmdir(temp_dir)

    return response


# 이미지 리사이즈 함수
def rescale_image(image, max_width):
    img = Image.open(image)
    # width_percent = (max_width / float(img.size[0]))
    # new_height = int((float(img.size[1]) * float(width_percent)))

    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * max_width)

    img = img.resize((max_width, dst_height), Image.LANCZOS)

    # 이미지를 BytesIO 객체에 저장
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')

    # BytesIO에서 InMemoryUploadedFile로 변환
    image_file = InMemoryUploadedFile(output_buffer, None, image.name, 'image/jpeg', output_buffer.tell(), None)

    return image_file

def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                image = rescale_image(image_file, 600)
                PostImage.objects.create(
                    post=post,
                    photo=image,
                )
            # 추가
            tag_string = request.POST.get("tags")
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
                for tag_name in tag_names:
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

                # 수정
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()

    context = {
        "form": form
    }
    return render(request, 'posts/post_add.html', context)


# 추가
def tags(request, tag_name):
    # 추가
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    # 추가
    else:
        posts = Post.objects.filter(tags=tag).order_by('-created')
        # 페이징 추가
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
        "tag_name": tag_name,
        "posts": posts,
        "page_obj": page_obj,
        "paginator": paginator,
        # 추가
        "custom_range": custom_range
    }

    return render(request, 'posts/tags.html', context)


# 추가
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    # 추가
    comment_form = CommentForm()
    context = {"post": post,
               "comment_form": comment_form, }
    return render(request, 'posts/post_detail.html', context)


# 추가
def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user.like_posts.filter(id=post.id).exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)
    url_next = request.GET.get("next") or reverse("posts:feeds") + f"#post-{post.id}"
    return HttpResponseRedirect(url_next)
