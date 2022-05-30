from django import forms
from .models import Community


class CommunityForm(forms.ModelForm):
    """Community model form"""
    class Meta:
        """Community model form meta options"""
        model = Community
        fields = ['name', 'description', 'bg_image', 'logo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'bg_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
