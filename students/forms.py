from django import forms
from courses.models import Course
from students.models import Student


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
        )


class StudentSignupForm(forms.ModelForm):
    """Describe form for Student.

    Arguments:
        forms.Form: superclass which describe form fields.
    """
    patronymic = forms.CharField(max_length=200)
    age = forms.IntegerField(min_value=0, max_value=150)
    phone = forms.CharField(min_length=11)
    city = forms.CharField(max_length=200)

    class Meta:
        model = Student
        fields = ['patronymic', 'age', 'phone', 'city']
