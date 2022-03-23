from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import Q
from profiles.models import Profile
from communities.models import Community

# Create your views here.
class SearchView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'search/search.html')
    def post(self, request, *args, **kwargs):
        search_type = request.POST.get('search_type')
        search_query = request.POST.get('search_query')
        if search_type == 'people':
            # need to check query against username, first_name, last_name
            profiles = Profile.objects.filter(
                Q(user__username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
            return render(request, 'search/search.html', {'search_results_people': profiles})
        if search_type == 'communities':
            communities = Community.objects.filter(name__icontains=search_query)
            return render(request, 'search/search.html', {'communities': communities})
        return HttpResponseRedirect(reverse('search'))