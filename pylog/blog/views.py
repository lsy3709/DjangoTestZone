from django.shortcuts import render, redirect
from blog.models import Post, Comment

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'post_list.html',context)

def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_content = request.POST["comment"]
        Comment.objects.create(
            post=post,
            content=comment_content
        )
    context = {
        "post" : post
    }
    return render(request, 'post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        # 추가
        # print(request.FILES)
        title = request.POST['title']
        content = request.POST['content']
        # 추가
        thumbnail = request.FILES['thumbnail']
        # 추가
        post = Post.objects.create(
            title=title,
            content=content,
            # 추가
            thumbnail=thumbnail
        )
        return redirect(f'/posts/{post.id}')
    else:
        print("method GET")
    return render(request, 'post_add.html')