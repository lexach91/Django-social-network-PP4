from django import forms
from .models import Profile


class ChangeAvatarForm(forms.ModelForm):
    """Change avatar form"""
    class Meta:
        """Change avatar form meta"""
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'multiple': False,
                'class': 'edit-avatar-btn'
            }),
        }


class EditProfileInfoForm(forms.ModelForm):
    """Edit profile info form"""
    class Meta:
        """Edit profile info form meta"""
        model = Profile
        fields = ['first_name', 'last_name',
                  'country', 'city', 'bio', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
