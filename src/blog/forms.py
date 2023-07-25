from django import forms
from .models import Post, Tag, Comment


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "제목을 입력해주세요.", "class": "form-control mt-40 mb-20"}),
            'content': forms.Textarea(attrs={'id': 'content'})
        }


class TagForm(forms.ModelForm):
    
    class Meta:
        model = Tag
        fields = ['content']


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={"placeholder": "댓글을 입력해주세요.", "class": "comment-input form-control"})
        }