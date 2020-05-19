"""Module for client requests handling."""
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from students.models import TeacherSchedule


def index(request):
    """Render index.html.

    Arguments:
        request: client request

    Returns:
        render(): render index.html page
    """
    return render(request, 'index.html', {})


@login_required
def profile(request):
    """Redirect to profile page to which group user belongs.

    Arguments:
        request: client request

    Returns:
        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Administrator
        then redirect to administrator/profile page TODO: test it

        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Teachers
        then redirect to courses/course_list/ page

        HttpResponseRedirect: if
        request.user.groups.filter(user=request.user)[0] = Students
        then redirect to students/student profile page
    """
    group = request.user.groups.filter(user=request.user)[0]

    if group.name == 'Administrator':
        return HttpResponseRedirect(reverse('administrator'))
    elif group.name == 'Teachers':
        return HttpResponseRedirect(reverse('course_list'))
    else:
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
                # FIXME: какая группа присваивается? Не происходит редирект
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
                    'id': 2,
                    'teacher_id': 1,
                    'start_timestamp': '2020-05-15T22:42:37.763Z',
                    'end_timestamp': '2020-05-15T23:27:37.763Z'
                },
                {
                    'id': 3,
                    'teacher_id': 1,
                    'start_timestamp': '2020-05-16T22:42:37.763Z',
                    'end_timestamp': '2020-05-16T23:27:37.763Z'
                }
            ]
        }

    """
    if api_version == 0:
        schedule = list(TeacherSchedule.objects.values(
                'id',
                'teacher_id',
                'start_timestamp',
                'end_timestamp',
                )
            )
        return JsonResponse({'shedule': schedule})
    else:
        return JsonResponse({})


class CalendarView(View):
    """Describe view for calendar.
    

    Arguments:
        View: dafault django superclass
    """

    template_name = 'calendar.html'

    def get(self, request):
        """Send list with teacher free day and time.

        Arguments:
            request: client request

        Resturns:
            render(): 
        """
        return render(
            request=request,
            template_name=self.template_name,
        )
    

    def post(self, request):
        """Reseive json with day and time.

        Student set time which he/she wants
        to do a free trial lesson

        Arguments:
            request: client request
        """
        print(request.POST)
