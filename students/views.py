"""Module where described the logic for user response."""
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.forms import CourseEnrollForm, StudentSignupForm, UserSignupForm
from courses.models import Course
from django.views.generic.detail import DetailView
from students.models import Student, Teacher
from guardian.shortcuts import assign_perm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from students.tokens import account_activation_token
from guardian.shortcuts import get_objects_for_user


def send_stats_to_email(request):
    """Send student's stats to email.

    TODO: Отправка информации о прохождении курсов(course_done),
    выполнении дз и полной статистики на емайл

    Как это пока работает:
    Пользователь делает запрос на отправку сообщения по email
    и пока отправляются только законченные курсы
    как будет добавлена зависимость по модели домашнего
    задания, можно будет делать выборку по многим зависимостям пользователя

    How to select done courses by student:

    from students.models import Student
    from courses.models import Course
    from guardian.shortcuts import get_objects_for_user
    student = Student.objects.get(name='testuser testuser')

    'courses.course_done'
        ^         ^
    app name | permission for model

    done_student_courses = get_objects_for_user(
        student.user, 'courses.course_done'
    )
    done_student_courses
    <QuerySet [<Course: Программирование 1-4 класс>]>

    Arguments:
        request: client request

    Returns:
        redirect: after sending a message redirect to 
        stats_email_sent
        
    """
    done_student_courses = get_objects_for_user(
        request.user,
        'courses.course_done',
    )
    email_subject = 'Please Activate Your Account'
    email_message = render_to_string(
        template_name='students/student/student_stats_to_email.html',
        context={
            'user': request.user,
            'courses': done_student_courses,
            },
        )
    request.user.email_user(email_subject, email_message)
    return redirect(to='stats_email_sent')


def stats_email_sent_view(request):
    """Render template when user sent stats to email.

    Arguments:
        request: client request

    Returns:
        render(): render 'stats_sent.html'
    """
    current_site = get_current_site(request)

    return render(
        request=request,
        template_name='students/student/stats_sent.html',
        context={'domain': current_site}
    )


def activation_sent_view(request):
    """Render template when activation code was sent to user.

    Arguments:
        request: client request

    Returns:
        render(): render 'activation_sent.html'
    """
    return render(
        request=request,
        template_name='students/student/activation_sent.html',
    )


def activate(request, uidb64, token):
    """Verifies the user and token.

    Note: We need specifi the backend for login(), here is
    native django backend auth, that is becauser we have
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',

    Arguments:
        request: client request
        uidb64: The primary key of the user, encoded in base 64
        token: token which was generated

    Returns:
        redirect(): if user exists and token is matched then redirect
        to students/student/

        render(): if user does not exist or token did not match
        then render activation_invalid.html
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.student.signup_confirmation = True
        user.save()
        login(
            request=request,
            user=user,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        return redirect(to='student')
    else:
        return render(
            request=request,
            template_name='students/student/activation_invalid.html',
        )


class StudentRegistrationView(View):
    """Class-based view for user signup."""

    template_name = 'students/student/registration.html'
    user_form_class = UserSignupForm
    student_form_class = StudentSignupForm

    def get(self, request):
        """GET-request treatment.

        Arguments:
            request: client request

        Returns:
            render(): render template html with empy forms
        """
        user_form = self.user_form_class
        student_form = self.student_form_class
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'user_form': user_form,
                'student_form': student_form,
            },
        )

    def post(self, request):
        """POST-request treatment.

        Arguments:
            request: client request

        Returns:
            redirect(): if forms are valid, user and student created,
            user authenticated and user is active redirect to
            /students/student/

            render(): if forms are not valid render the template
            html with forms contains errors
        """
        user_form = self.user_form_class(request.POST)
        student_form = self.student_form_class(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()

            students_group = Group.objects.get(name='Students')
            students_group.user_set.add(user)

            student_form.save(commit=False)
            student = Student.objects.create(
                user=user,
                name=student_form.cleaned_data.get('name'),
                age=student_form.cleaned_data.get('age'),
                phone=student_form.cleaned_data.get('phone'),
                city=student_form.cleaned_data.get('city'),
            )
            student.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Please Activate Your Account'
            email_message = render_to_string(
                template_name='students/student/activation_request.html',
                context={
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(
                        user=user
                        ),
                    },
                )
            user.email_user(email_subject, email_message)
            return redirect(to='activation_sent')
        # FIXME: здесь ошибка при рендере пришло 8 значений, а надо 2
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'user_form': user_form,
                'student_form': student_form,
            },
        )


@login_required(login_url='/accounts/login/')
def get_profile(request):
    # student = Student.objects.get(user=request.user)
    student = get_object_or_404(Student, user=request.user)
    return render(
        request=request,
        template_name='students/student/profile.html',
        context={'student': student},
        )


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data.get('course')
        self.course.students.add(self.request.user)
        return super(
            StudentEnrollCourseView,
            self,
            ).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail',
            args=[self.course.id]
            )


@login_required(login_url='/accounts/login/')
def get_courses_list(request):
    """Returns courses list.

    Arguments:
        request: client request

    Returns:
        render(): render list.html with courses list which
        contains user.student
    """
    courses = Course.objects.filter(
        students__in=[request.user],
        )
    return render(
        request=request,
        template_name='students/course/list.html',
        context={'object_list': courses},
    )


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        query_set = super(StudentCourseDetailView, self).get_queryset()
        return query_set.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        # get course object
        course = self.get_object()

        context['user_permission'] = []
        for cur_module in course.modules.all():
            context['user_permission'].append(self.request.user.has_perm('view_current_module', cur_module))

        if 'module_id' in self.kwargs:
        # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
        # get first module
            context['module'] = course.modules.all()[0]
            assign_perm('view_current_module', context['user'], context['module'])
        return context
