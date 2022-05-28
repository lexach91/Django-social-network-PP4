from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/feed/')
        return render(request, 'home/home.html', {})
