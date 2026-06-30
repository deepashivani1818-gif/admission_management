from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'phone',
            'course',
            'address',
            'father_name',
            'mother_name',
            'dob',
            'gender',
            'marksheet',
        ]