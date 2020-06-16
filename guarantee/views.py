"""Module for client requests handling."""
import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from guardian.shortcuts import get_objects_for_user

from courses.models import LessonRoom, Subject, Course
from students.forms import TeacherEditForm
from students.models import Schedule, Student, Teacher


def index(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='index.html',
        context={'subjects': subjects, 'courses': courses},
    )


def our_approach(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='approach.html',
        context={'subjects': subjects, 'courses': courses},
    )


def our_teachers(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='teachers.html',
        context={'subjects': subjects, 'courses': courses},
    )


def our_testimonials(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='testimonials.html',
        context={'subjects': subjects, 'courses': courses},
    )


def our_results(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='results.html',
        context={'subjects': subjects, 'courses': courses},
    )


def camp(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    return render(
        request=request,
        template_name='camp.html',
        context={'subjects': subjects, 'courses': courses},
    )




@login_required
def profile(request):
    """Redirect to profile page to which group user belongs.

    Arguments:
        request: client request

    Returns:
        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Managers
        then redirect to administrator/profile page

        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Teachers
        then redirect to courses/ page

        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Students
        then redirect to students/ profile page
    """
    group = request.user.groups.filter(user=request.user)[0]

    if group.name == 'Managers':
        return HttpResponseRedirect(reverse('manager'))
    elif group.name == 'Teachers':
        return HttpResponseRedirect(reverse('teacher'))
    elif group.name == 'Students':
        return HttpResponseRedirect(reverse('student'))
    context: dict = {}
    template = 'profile.html'
    return render(request, template, context)


class CustomLoginView(View):
    """Custom LoginView for handling the login amout.

    Arguments:
        View: default view superclass
    """

    form_class = AuthenticationForm()
    template_name = 'registration/login.html'

    def get(self, request):
        """Handle GET-request.

        next_try is amount of user login trying, it is increments
        then user have paste wrong login, password

        Arguments:
            request: client request

        Returns:
            redirect(): if user is authenticated, then
            redirect to index page

            render(): if user is not authenticated, then
            return empty AuthenticationForm instance
        """
        next_try: int = 0

        if request.user.is_authenticated:
            return redirect(to='index')
        form = self.form_class
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': form,
                'next': next_try,
            },
        )

    def post(self, request):
        """Handle POST-request.

        Arguments:
            request: client request

        Returns:
            redirect(): if form valid, user exists and user is not blocked
            redirect to 'profile'

            render(): if form is not valid or no user or user is blocked
            then return form and render page, where is form.errors
            which describes the problem
        """
        next_try: int = int(request.POST.get('next'))
        next_try += 1

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user and user.is_active:
                login(request, user)
                next_try = 0
                return redirect(to='profile')
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': form,
                'next': next_try,
            },
        )


def get_json_busy_datetime(request, api_version):
    """Returns json-file with teachers busy datetime.

    Arguments:
        request: client request

    Returns:
        JsonResponse (json):
        {
            'shedule': [
                {
                    'start_timestamp': '2020-05-15T22:42:37.763Z',
                    'end_timestamp': '2020-05-15T23:27:37.763Z'
                },
                {
                    'start_timestamp': '2020-05-16T22:42:37.763Z',
                    'end_timestamp': '2020-05-16T23:27:37.763Z'
                }
            ]
        }

    """
    if api_version == 0:
        try:
            schedule = list(Schedule.objects.values(
                'start_timestamp', 'end_timestamp',
                ).distinct(),
            )
        except DatabaseError:
            schedule = []

        return JsonResponse({'shedule': schedule})

    return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class CalendarView(View):
    """Describe view for calendar.

    !!!! Note: I don't use csrf-token now, look at 
        csrf_exempt decorator    

    Arguments:
        View: default django superclass
    """

    get_template_name = 'calendar.html'
    post_template_name = 'trial_lesson_approved.html'

    def get(self, request):
        """Send list with teacher free day and time.

        Arguments:
            request: client request

        Resturns:
            render(): 
        """
        return render(
            request=request,
            template_name=self.get_template_name,
        )
    

    def post(self, request):
        """Reseive json with day and time.

        Student set time which he/she wants
        to do a free trial lesson

        For creating a schedule of new students, I use teacher
        with name schedule_teacher, when manager can change a
        instance of teacher. Also, I make a 
        end_timestamp = start_timestamp + 45min. If manager wants to 
        change value it could be.

        schedule_teacher is not real person.

        TODO: form for validation a client request.
        TODO: change render to redirect('lesson_approved')
        TODO: render() does not work
        FIXME: datetime.datetime to timezone, now I don't use tz
        but it should

        A Unix timestamp is the number of seconds between a particular
        date and January 1, 1970 at UTC. You can convert
        a timestamp to date using fromtimestamp() method.

        JS from calendar.js:
        const data={
                parent_name: parents_name,
                student_name: kids_name,
                phone: phone,
                start_timestamp: Date.now(), <- !!!returns milliseconds
            };

        Arguments:
            request: client request
        """
        user = User.objects.get(name='schedule_user')

        parent_name = request.POST.get('parent_name')
        parent_phone = request.POST.get('phone')
        student_name = request.POST.get('student_name')

        comment = '{0} имя родителя,\
            {1} тел. родителя,\
            {2} имя ученика'.format(
                parent_name, parent_phone, student_name,
            )

        start_timestamp = datetime.datetime.fromtimestamp(
            int(request.POST.get('start_timestamp')) / 1000.0,
        )
        
        end_timestamp = (start_timestamp + datetime.timedelta(minutes=45))

        schedule = Schedule.objects.create(
            user=user,
            comment=comment,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        schedule.save()
        
        return render(
            request=request,
            template_name=self.post_template_name,
        )


@login_required
def teacher(request):
    template_name = 'teacher/profile.html'

    upcoming_lessons = LessonRoom.objects.filter(
        teacher=request.user.teacher,
        schedule__start_timestamp__gte=timezone.now(),
    )
    students = request.user.teacher.students.all()

    for student in students:

        done_modules = get_objects_for_user(
            student.user, 'courses.module_done',
        )

        student_courses = student.courses_joined.all()

        for course in student_courses:
            percent = (100 * (course.modules.intersection(
                done_modules)).count()) / course.modules.all().count()
            course.done_percent = '{0}%'.format(percent)

        student.student_courses = [*student_courses]

    return render(
        request=request,
        template_name=template_name,
        context={
            'teacher': request.user.teacher,
            'upcoming_lessons': upcoming_lessons,
            'students': students,
        },
    )


def get_lead_list_json(request, api_version):
    """Return a lead list in json.

    Arguments:
        request {[type]} -- [description]
        api_version (int): api version
    """
    if api_version == 0:
        try:
            lead_list = list(Student.objects.filter(
                    status__name='lead',
                ).values()
            )
        except DatabaseError:
            lead_list = []

        return JsonResponse(lead_list, safe=False)

    return JsonResponse({'error': 'wrong api version'})


@method_decorator(csrf_exempt, name='dispatch')
class TeacherProfileEditView(View):
    template_name = 'teacher/edit_profile.html'

    def get(self, request):
        return render(
            request=request,
            template_name=self.template_name,
            context={'teacher': request.user.teacher},
        )

    def post(self, request):
        form = TeacherEditForm(
            data=request.POST, instance=request.user.teacher,
        )
        if form.is_valid():
            teacher = form.save()
            teacher.save()
        return redirect(to='teacher')
