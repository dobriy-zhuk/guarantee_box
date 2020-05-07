from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View


def index(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    group = request.user.groups.filter(user=request.user)[0]

    if group.name == "Administrator":
        return HttpResponseRedirect(reverse('administrator'))
    elif group.name == "Teachers":
        return HttpResponseRedirect(reverse('course_list'))
    elif group.name == "Students":
        return HttpResponseRedirect(reverse('student'))

    context = {}
    template = "profile.html"
    return render(request, template, context)


class CustomLoginView(View):
# TODO: добавить проверку на количество повторений == 5 раз заморозка на 30 секунд
# TODO: добавить функцию восстановления пароля по email
    """Custom LoginView for handling the login amout.

    Arguments:
        View: default view superclass 
    """
    form_class = AuthenticationForm()
    template_name = 'registration/login.html'

    def get(self, request):
        """Handling GET-request.

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
        next_try = 0

        if request.user.is_authenticated:
            return redirect(to='index')
        else:
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
        """Handling POST-request.

        Arguments:
            request: client request

        Returns:
            redirect(): if form valid, user exists and user is not blocked
            redirect to 'profile'

            render(): if form is not valid or no user or user is blocked
            then return form and render page, where is form.errors
            which describes the problem
        """
        next_try = int(request.POST.get('next'))
        next_try += 1

        form = AuthenticationForm(request, data=request.POST)
        import pdb
        pdb.set_trace()

        while next_try <= 5:
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password'),
                )
                if user and user.is_active:
                    login(request, user)
                    next_try = 0
                    return redirect(to='profile')
            else:
                return render(
                    request=request,
                    template_name=self.template_name,
                    context={
                        'form': form,
                        'next': next_try,
                        }
                )
        else:
            return render(
                request=request,
                template_name=self.template_name,
                context={
                    'form': form,
                    'next': next_try,
                    'do_clock': True,
                }
            )
