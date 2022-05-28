from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'post_type', 'community', 'profile']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'What\'s on your mind?'
            }),
            'image': forms.ClearableFileInput(
                attrs={'multiple': False, 'accept': 'image/*'}
            ),
            'post_type': forms.HiddenInput(),
            'community': forms.HiddenInput(),
            'profile': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }
