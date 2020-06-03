from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Count
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from opentok import OpenTok

from students.forms import CourseEnrollForm

from courses.forms import ModuleFormSet
from courses.models import Content, Course, Module, Subject, LessonRoom


def check_user_group(user):
    group = user.groups.filter(user=user)[0]
    return group.name == 'Teachers' 


# Create your views here.
def post_coding(request):
    return render(request, 'index.html', {})


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user.teacher)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user.teacher
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user.teacher)
        return super(CourseModuleUpdateView,
                 self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """Describe here!!!

    Arguments:
        TemplateResponseMixin {[type]} -- [description]
        View {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'


    def get_model(self, model_name):
        content_list = [
            'text', 'video', 'image', 'file',
            'question', 'blockly', 'c_plus_plus', 'drag_and_drop',
        ]
        if model_name in content_list:
            return apps.get_model(
                app_label='courses',
                model_name = model_name,
            )
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id = None):
        self.module = get_object_or_404(
            Module,
            id = module_id,
            course__owner = request.user.teacher,
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model,
                id = id,
                # owner = request.user.teacher,
                owner = request.user,
            )
        return super(ContentCreateUpdateView, self).dispatch(
            request, module_id, model_name, id
        )

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {
                'form': form,
                'object': self.obj,
                'model': model_name,
            }
        )

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj, data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.owner = request.user.teacher
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(
                    module=self.module,
                    item = obj
                )
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user.teacher
        )
        module = content.module
        content.item.delete()
        content.delete()
        
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user.teacher)
        return self.render_to_response({'module': module})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses,
            },
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            CourseDetailView,
            self,
            ).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object},
                )

        return context


@login_required(login_url='/accounts/login/')
@user_passes_test(check_user_group, login_url='/accounts/login/')
def get_lesson(request):
    """[summary]

    TODO: class-based view get, post requests

    Note:
        session_id (str): len(session_id) = 73
        token (str): len(token) = 340

    TODO: request should be POST because we need receive list of students

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    #Записать в БД. Вернуть localhost:3000 в качестве страницы!!!

    opentok = OpenTok("46769324", "0a5d254d5d11b7e1ef22004df51b6e28f9279823")
    session = opentok.create_session()

    session_id = session.session_id
    token = opentok.generate_token(session_id)

    lesson_room = LessonRoom.objects.create(
        lesson_name='',
        teacher=request.user.teacher,
        session_id=session_id,
        token=token,
    )
    lesson_room.save()
    # TODO: lesson_room.students.add(1, 2) <- students ids

    return render(
        request=request,
        template_name='courses/course/lesson.html',
        context={"session_id": session_id, "token": token, "api_key": "46769324"}
    )
