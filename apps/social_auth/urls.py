from django.urls import path, re_path

from apps.social_auth.views import LoginUserView, SocialUserListView

urlpatterns = [
    re_path('auth/login/?$', LoginUserView.as_view(), name='login'),
    re_path('auth/user/?$', SocialUserListView.as_view(), name='signup'),
]
