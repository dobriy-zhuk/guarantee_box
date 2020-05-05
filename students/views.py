from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.forms import CourseEnrollForm, StudentSignupForm
from courses.models import Course
from django.views.generic.detail import DetailView
from students.models import Student
from guardian.shortcuts import assign_perm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View


class StudentRegistrationView(View):
    template_name = 'students/student/registration.html'
    user_form_class = UserCreationForm
    student_form_class = StudentSignupForm
    success_url = reverse_lazy('student_course_list')

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
                }
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
        # import pdb
        # pdb.set_trace()
        if user_form.is_valid() and student_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = user_form.save()
            student_form.save(commit=False)
            student = Student.objects.create(
                user=user,
                patronymic = student_form.cleaned_data.get('patronymic'),
                age = student_form.cleaned_data.get('age'),
                phone = student_form.cleaned_data.get('phone'),
                city = student_form.cleaned_data.get('city'),
            )
            student.save()
            user = authenticate(
                username=username,
                password=password,
            )
            if user and user.is_active:
                login(request, user)
                return redirect(to='student')
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'user_form': user_form,
                'student_form': student_form,
            }
        )


    # def form_valid(self, form):
    #     result = super(StudentRegistrationView,
    #                    self).form_valid(form)
    #     cleaned_data_from_form = form.cleaned_data
    #     user = authenticate(
    #         username=cleaned_data_from_form.get('username'),
    #         password=cleaned_data_from_form.get('password1'),
    #         )
    #     login(self.request, user)
    #     return result


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
