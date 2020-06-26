from django import forms
from students.models import Student


class NewLeadForm(forms.ModelForm):
    """Describe form for new Lead.

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