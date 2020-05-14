from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Instructor


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class ProfileImgForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic', ]


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['about_yourself', 'age', 'bank_account_name',
                  'bank_name', 'bank_account_number', 'bank_account_type', 'IFSC_code']


class SupportForm(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField()
    issue = forms.CharField(max_length=2000)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))
