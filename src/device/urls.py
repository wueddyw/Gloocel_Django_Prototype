from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from device import views

urlpatterns = [
 path('', views.DeviceList.as_view()),
 path('<str:pk>/', views.DeviceDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
