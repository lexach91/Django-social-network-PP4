from django.shortcuts import render
from django.views import View
from profiles.models import Profile
from communities.models import Community

# Create your views here.
class SearchView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'search/search.html')
