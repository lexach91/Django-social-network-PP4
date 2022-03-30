from pyexpat import model
from attr import field
from django import forms
from matplotlib import widgets
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': widgets.Textarea(attrs={'rows': 3, 'cols': 40}),
            'image': widgets.FileInput(attrs={'accept': 'image/*'})
        }