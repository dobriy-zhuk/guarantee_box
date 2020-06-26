from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('applicants/', views.ApplicantListView.as_view(), name='applicants'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('leads/', views.Leads.as_view(), name='leads'),
    path('lead/new/', views.NewLead.as_view(), name='add_new_lead'),
]