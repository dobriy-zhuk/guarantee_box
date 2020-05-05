from django import forms
from courses.models import Course
from students.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
    name = forms.CharField(max_length=200)
    age = forms.IntegerField(min_value=0, max_value=150)
    phone = forms.CharField(min_length=11)
    city = forms.CharField(max_length=200)

    class Meta:
        model = Student
        fields = ('name', 'age', 'phone', 'city')


class UserSignupForm(UserCreationForm):
    """Describe form for User.

    Arguments:
        UserCreationForm: superclass which describe form fields.
    """
    email = forms.EmailField(max_length=150)

    class Meta:
        """Metadata class.

        When Django make UserSignupForm class,
        Meta collects fields form User model.
        """
        model = User
        fields = (
            'username', 'email',
            'password1', 'password2',
            )
