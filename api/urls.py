from django.urls import path
from . import views


urlpatterns = [
    path('live_video/', views.LeadListCreate.as_view()),
]