from django.shortcuts import render
from django.views import View
from .models import Community
from posts.forms import PostForm, CommentForm


class UsersCommunitiesView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        communities = Community.objects.filter(members__in=[user])
        return render(request, 'communities/users_communities.html', {'communities': communities})


class CommunityView(View):
    def get(self, request, slug, *args, **kwargs):
        community = Community.objects.get(slug=slug)
        post_form = PostForm()
        comment_form = CommentForm()
        context = {
            'community': community,
            'post_form': post_form,
            'comment_form': comment_form,
        }
        return render(request, 'communities/community.html', context)