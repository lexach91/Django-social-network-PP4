from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from profiles.models import Profile
from communities.models import Community

# Create your views here.
class SearchView(View):
    def get(self, request, *args, **kwargs):
        # get all profiles that request.user is not friends with and himself
        profiles = Profile.objects.exclude(
            friends__in=[request.user.profile]
        ).exclude(
            user=request.user
        )
        # get all communities that request.user is not members of
        communities = Community.objects.exclude(
            members__in=[request.user]
        )
            
        return render(request, 'search/search.html', {'profiles': profiles, 'communities': communities})
    # def post(self, request, *args, **kwargs):
    #     search_type = request.POST.get('search_type')
    #     search_query = request.POST.get('search_query')
    #     if search_type == 'people':
    #         if search_query:
    #             profiles = Profile.objects.filter(
    #                 Q(user__username__icontains=search_query) |
    #                 Q(first_name__icontains=search_query) |
    #                 Q(last_name__icontains=search_query) |
    #                 Q(first_name__icontains=search_query.split()[0], last_name__icontains=search_query.split()[-1]) |
    #                 Q(first_name__icontains=search_query.split()[-1], last_name__icontains=search_query.split()[0])
    #             )
    #             return render(request, 'search/search.html', {'search_results_people': profiles})
    #         profiles = Profile.objects.all()
    #         return render(request, 'search/search.html', {'search_results_people': profiles})
    #     if search_type == 'communities':
    #         if search_query:
    #             communities = Community.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    #             return render(request, 'search/search.html', {'search_results_communities': communities})
    #         communities = Community.objects.all()
    #         return render(request, 'search/search.html', {'search_results_communities': communities})
    #     return HttpResponseRedirect(reverse('search:search'))
    
    
class SearchPeopleAjax(View):
    def post(self, request, *args, **kwargs):
        search_query = request.POST.get('search_query')
        profiles = Profile.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query.split()[0], last_name__icontains=search_query.split()[-1]) |
            Q(first_name__icontains=search_query.split()[-1], last_name__icontains=search_query.split()[0])
        )
        if not search_query:
            profiles = Profile.objects.all()
        profiles_json = [{'username': profile.user.username, 'name': str(profile), 'avatar': profile.avatar_url} for profile in profiles]
        return JsonResponse({'profiles': profiles_json})
    
class SearchCommunitiesAjax(View):
    def post(self, request, *args, **kwargs):
        search_query = request.POST.get('search_query')
        communities = Community.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if not search_query:
            communities = Community.objects.all()
        communities_json = [{'name': community.name, 'logo': community.logo_url, 'slug': community.slug } for community in communities]
        return JsonResponse({'communities': communities_json})
        
        