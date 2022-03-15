from django.shortcuts import render
from django.views import View

from .models import Profile
# Create your views here.

class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/my_profile.html', {})