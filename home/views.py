from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


class HomeView(View):
    """Class based view for the home page"""

    def get(self, request, *args, **kwargs):
        """GET method for the home page"""
        if request.user.is_authenticated:
            return HttpResponseRedirect('/feed/')
        return render(request, 'home/home.html', {})
