from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'post_type', 'community', 'profile']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'post_type': forms.HiddenInput(),
            'community': forms.HiddenInput(),
            'profile': forms.HiddenInput(),
        }
