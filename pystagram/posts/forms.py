from django import forms
# 추가
from posts.models import Comment, Post, PostImage, Message


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'post',
        ]


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'sender'
        ]




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['photo']
