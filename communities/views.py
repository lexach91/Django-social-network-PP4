from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from .models import Community
from posts.forms import PostForm, CommentForm
from .forms import CommunityForm
from feed.models import (
    CommunityCreateEvent,
    CommunityJoinEvent,
    CommunityLeaveEvent,
    CommunityDeleteEvent
)


class UsersCommunitiesView(View):
    """Class based view for users_communities page"""

    def get(self, request, *args, **kwargs):
        """GET method for users_communities page"""
        user = request.user
        communities = Community.objects.filter(members__in=[user])
        return render(
            request,
            'communities/users_communities.html',
            {'communities': communities}
        )


class CommunityView(View):
    """Class based view for community page"""

    def get(self, request, slug, *args, **kwargs):
        """GET method for community page"""
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
    """Class based ajax view for joining community"""

    def post(self, request, *args, **kwargs):
        """POST method for joining community"""
        if request.is_ajax():
            community_id = request.POST.get('community_id')
            community = Community.objects.get(id=community_id)
            community.members.add(request.user)
            community.save()
            community_join_event = CommunityJoinEvent.objects.create(
                initiator=request.user,
                community=community,
            )
            community_join_event.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class LeaveCommunityView(View):
    """Class based ajax view for leaving community"""

    def post(self, request, *args, **kwargs):
        """POST method for leaving community"""
        if request.is_ajax():
            community_id = request.POST.get('community_id')
            community = Community.objects.get(id=community_id)
            community.members.remove(request.user)
            community.save()
            community_leave_event = CommunityLeaveEvent.objects.create(
                initiator=request.user,
                community=community,
            )
            community_leave_event.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class CreateCommunityView(View):
    """Class based view for creating community"""

    def get(self, request, *args, **kwargs):
        """GET method for creating community"""
        form = CommunityForm()
        return render(
            request,
            'communities/create_community.html',
            {'form': form}
        )

    def post(self, request, *args, **kwargs):
        """POST method for creating community"""
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            community.members.add(request.user)
            community.save()
            community_create_event = CommunityCreateEvent.objects.create(
                initiator=request.user,
                community=community,
            )
            community_create_event.save()
            return HttpResponseRedirect(f'/communities/{community.slug}/')


class EditCommunityView(View):
    """Class based view for editing community"""

    def get(self, request, slug, *args, **kwargs):
        """GET method for editing community"""
        community = Community.objects.get(slug=slug)
        if request.user == community.creator:
            form = CommunityForm(instance=community)
            return render(
                request,
                'communities/create_community.html',
                {'form': form, 'community': community}
            )
        return HttpResponseRedirect(f'/communities/{community.slug}/')

    def post(self, request, slug, *args, **kwargs):
        """POST method for editing community"""
        community = Community.objects.get(slug=slug)
        if request.user == community.creator:
            form = CommunityForm(
                request.POST, request.FILES, instance=community)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/communities/{community.slug}/')
            return render(
                request,
                'communities/create_community.html',
                {'form': form, 'community': community}
            )
        return HttpResponseRedirect(f'/communities/{community.slug}/')


class DeleteCommunityView(View):
    """Class based view for deleting community"""

    def post(self, request, slug, *args, **kwargs):
        """POST method for deleting community"""
        community = Community.objects.get(slug=slug)
        if request.user == community.creator:
            community_delete_event = CommunityDeleteEvent.objects.create(
                initiator=request.user,
            )
            community_delete_event.save()
            community.delete()
            return HttpResponseRedirect('/communities/')
        return HttpResponseRedirect(f'/communities/{community.slug}/')
