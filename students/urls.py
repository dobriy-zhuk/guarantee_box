from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_profile, name='student'),
    path('payment/', views.get_payment, name='payment'),
    path('lesson/', views.get_lesson, name='student_lesson'),
    path(
         'send-stats/',
         views.send_stats_to_email,
         name='send_email_stats',
     ),
    path(
         'sent-stats/',
         views.stats_email_sent_view,
         name='stats_email_sent',
     ),
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         views.get_courses_list,
         name='student_course_list'),
    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path(
         'activate/<slug:uidb64>/<slug:token>/',
         views.activate,
         name='activate',
     ),
    path(
         'available-lessons/',
         views.get_available_lessons,
         name='available_lessons',
     ),
    path(
         'api/<int:api_version>/<int:student_id>/<module_id>/<int:attempt>/',
         views.set_student_reward_card,
         name='set_student_reward_card',
    )
]
