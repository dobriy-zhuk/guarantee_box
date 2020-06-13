from django.urls import path

from students import views

urlpatterns = [
    path('student/', views.get_profile, name='student'),
    path(
         'edit-profile/', views.StudentProfileEditView.as_view(),
         name='edit_student_profile',
     ),
    path('payment/', views.get_payment, name='payment'),
    path('payment/', views.get_payment, name='payment'),
    path('webrtc/', views.get_webrtc, name='get_webrtc'),
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
         'api/<int:api_version>/set-reward-card/<int:student_id>/<int:lesson_id>/<int:attempt>/',
         views.set_student_reward_card,
         name='set_student_reward_card',
     ),
    path(
         'api/<int:api_version>/get-lesson-info/<int:lesson_id>/',
         views.get_lesson_room_info,
         name='get_lesson_room_info',
    ),   
    path(
         'api/<int:api_version>/decrease-reward-card-amount/<int:student_id>/<int:amount>/',
         views.decrease_student_reward_card_amount,
         name='decrease_student_reward_card_amount',
    ),
    path(
         'api/<int:api_version>/student-payment/',
         views.StudentPaymentAPI.as_view(),
         name='student_payment',
    ),
    path(
         'api/<int:api_version>/set-student-module-done/',
         views.set_student_module_done,
         name='set_student_module_done',
    ),
]
