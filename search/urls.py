from django.urls import path
from .views import SearchView, SearchPeopleAjax, SearchCommunitiesAjax


urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('people/', SearchPeopleAjax.as_view(), name='search_people_ajax'),
    path('communities/', SearchCommunitiesAjax.as_view(),
         name='search_communities_ajax'),
]
