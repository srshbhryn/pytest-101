from django import forms

from courses.models import Course
from accounts.models import User

class AddStudentForm(forms.Form):

    course = Course.objects
    student = forms.ChoiceField()
