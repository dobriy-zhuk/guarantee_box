from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    import pdb
    pdb.set_trace()
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