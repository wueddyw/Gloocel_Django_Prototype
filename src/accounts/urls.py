from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views
from rest_framework.authtoken import views as authViews

urlpatterns = [
    path('register', views.RegisterAPI.as_view()),
    path('login', views.login_api),
    path('logout', views.LogoutAPI.as_view()),
    path('verify', views.VerifyAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
