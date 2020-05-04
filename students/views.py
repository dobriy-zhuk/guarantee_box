from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from courses.models import Course
from django.views.generic.detail import DetailView
from .models import Student
from guardian.shortcuts import assign_perm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


class StudentRegistrationView(CreateView):
    # TODO: сделать регистрацию пользователя
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView,
                       self).form_valid(form)
        cleaned_data_from_form = form.cleaned_data
        user = authenticate(
            username=cleaned_data_from_form.get('username'),
            password=cleaned_data_from_form.get('password1'),
            )
        login(self.request, user)
        return result


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


class StudentCourseListView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        query_set = super(
            StudentCourseListView,
            self
            ).get_queryset()
        return query_set.filter(students__in=[self.request.user])


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
