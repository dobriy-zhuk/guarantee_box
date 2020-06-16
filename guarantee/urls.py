"""Guarantee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from guarantee_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from guarantee import views

urlpatterns = [
    path('', views.index, name='index'),
    path('approach/', views.our_approach, name='our_approach'),
    path('results/', views.our_results, name='our_results'),
    path('testimonials/', views.our_testimonials, name='our_testimonials'),
    path('teachers/', views.our_teachers, name='our_teachers'),
    path('profile/', views.profile, name='profile'),
    path('camp/', views.camp, name='camp'),
    path('teacher/', views.teacher, name='teacher'),
    path(
        'teacher/edit-profile',
        views.TeacherProfileEditView.as_view(),
        name='teacher_edit_profile',
    ),
    path(
        'accounts/login/',
        views.CustomLoginView.as_view(),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('managers/', include('managers.urls')),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset/confirm/<slug:uidb64>/<slug:token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
         'calendar/',
         views.CalendarView.as_view(),
         name='student_calendar'
    ),
    path(
         'api/<int:api_version>/get-schedule/',
         views.get_json_busy_datetime,
         name='api_get_schedule'
    ),
    path(
         'api/<int:api_version>/get-lead-list/',
         views.get_lead_list_json,
         name='api_get_lead_list'
    ),
    path('i18n/', include('django.conf.urls.i18n')),
]


# urlpatterns += i18n_patterns('',
#     # (_('dual-lang/'), include('duallang.urls')),
#     path('', include('guarantee.urls')),
# )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
