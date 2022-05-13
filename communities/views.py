from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from .models import Community
from posts.forms import PostForm, CommentForm
from .forms import CommunityForm


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
        posts = community.posts.all()
        context = {
            'community': community,
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': posts
        }
        return render(request, 'communities/community.html', context)
    

class JoinCommunityView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            community_id = request.POST.get('community_id')
            community = Community.objects.get(id=community_id)
            community.members.add(request.user)
            community.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    
class LeaveCommunityView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            community_id = request.POST.get('community_id')
            community = Community.objects.get(id=community_id)
            community.members.remove(request.user)
            community.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class CreateCommunityView(View):
    def get(self, request, *args, **kwargs):
        form = CommunityForm()
        return render(request, 'communities/create_community.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.logo = form.cleaned_data['logo']
            community.bg_image = form.cleaned_data['bg_image']
            community.save()
            community.members.add(request.user)
            community.save()
            return HttpResponseRedirect(f'/communities/{community.slug}/')
            
class EditCommunityView(View):
    def get(self, request, slug, *args, **kwargs):
        community = Community.objects.get(slug=slug)
        form = CommunityForm(instance=community)
        return render(request, 'communities/create_community.html', {'form': form, 'community': community})
    
    def post(self, request, slug, *args, **kwargs):
        community = Community.objects.get(slug=slug)
        form = CommunityForm(request.POST, request.FILES, instance=community)
        print(request.POST)
        print(request.FILES)
        # print(form.cleaned_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/communities/{community.slug}/')