from django import forms
# 추가
from posts.models import Comment, Post, PostImage, Message


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'post',
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': '댓글 달기...',
                }
            )
        }

class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': '쪽지 내용...',
                }
            )
        }



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
