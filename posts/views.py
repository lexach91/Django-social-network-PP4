from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post
from .forms import PostForm


# Create your views here.
class CreatePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})