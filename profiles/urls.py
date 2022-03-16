from django.urls import URLPattern, path
from .views import MyProfileView, UserProfileView

urlpatterns = [
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
]