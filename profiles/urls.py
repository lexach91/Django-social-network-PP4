from django.urls import URLPattern, path
from .views import MyProfileView

urlpatterns = [
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
]