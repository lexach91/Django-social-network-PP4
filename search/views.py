from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from profiles.models import Profile
from communities.models import Community

# Create your views here.


class SearchView(View):
    """Class based view for a search page"""

    def get(self, request, *args, **kwargs):
        """Get method for search page"""
        # get all profiles that request.user is not friends with
        profiles = Profile.objects.exclude(
            friends__in=[request.user.profile]
        ).exclude(
            user=request.user
        )
        # get all communities that request.user is not members of
        communities = Community.objects.exclude(
            members__in=[request.user]
        )

        context = {
            'profiles': profiles,
            'communities': communities,
        }
        return render(request, 'search/search.html', context)


class SearchPeopleAjax(View):
    """Class based ajax handler for searching people"""

    def post(self, request, *args, **kwargs):
        """Post method for searching people"""
        search_query = request.POST.get('search_query')
        profiles = Profile.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(
                first_name__icontains=search_query.split()[0],
                last_name__icontains=search_query.split()[-1]
            ) |
            Q(
                first_name__icontains=search_query.split()[-1],
                last_name__icontains=search_query.split()[0]
            )
        )
        if not search_query:
            # on empty search query, return all profiles
            profiles = Profile.objects.all()
        profiles_json = [
            {
                'username': profile.user.username,
                'name': str(profile),
                'avatar': profile.avatar_url,
                'online': profile.online
            } for profile in profiles
        ]
        return JsonResponse({'profiles': profiles_json})


class SearchCommunitiesAjax(View):
    """Class based ajax handler for searching communities"""

    def post(self, request, *args, **kwargs):
        """Post method for searching communities"""
        search_query = request.POST.get('search_query')
        communities = Community.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query))
        if not search_query:
            # on empty search query, return all communities
            communities = Community.objects.all()
        communities_json = [{
            'name': community.name,
            'logo': community.logo_url,
            'slug': community.slug,
            'description': community.description,
            'member_count': community.member_count,
        } for community in communities]
        return JsonResponse({'communities': communities_json})
