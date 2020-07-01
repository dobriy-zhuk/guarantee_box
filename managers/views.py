from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from managers.models import Manager
from students.models import Teacher, Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View


@login_required(login_url='/accounts/login/')
def manager(request):

    return render(
        request=request,
        template_name='managers/main/profile.html',
        context={'manager': request.user.manager},
    )


class ApplicantListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'managers/main/applicant.html'
    queryset = Teacher.objects.filter(status__name='Applicant')
    context_object_name = 'applicant_list'


class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'managers/main/teachers.html'
    queryset = Teacher.objects.filter(status__name='Teacher')
    context_object_name = 'teacher_list'


class Leads(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'managers/main/leads.html'
    queryset = Student.objects.filter(status__name='Lead')
    context_object_name = 'lead_list'


class Students(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'managers/main/students.html'
    queryset = Student.objects.filter(status__name='Student')
    context_object_name = 'student_list'


class NewLead(LoginRequiredMixin, View):
    template_name = 'managers/main/new_lead.html'

    def get(self, request):
        return render(
            request=request,
            template_name=self.template_name,
        )

    def post(self, request):
        pass