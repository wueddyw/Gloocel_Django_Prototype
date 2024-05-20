from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from door import views

urlpatterns = [
  path('', views.DoorList.as_view()),
  path('open/<int:pk>', views.DoorOpen.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)