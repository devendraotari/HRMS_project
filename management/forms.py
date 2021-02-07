from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from management.models import Employee, LeaveConf, Compose, Notify
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserLoginForm(AuthenticationForm):
    model = User
    fields = ('username', 'password')
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserLoginForm, self).__init__(*args, **kwargs)
    #
    # username = forms.EmailField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': '',
    #         'id': 'password',
    #     }
    # ))
    #


class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' Re-type password'}),

        }

    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE : errors here will appear in 'non_field_errors()'
        """
        cleaned_data = super(UserRegisterForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        print("saving user")
        if commit:
            user.save()
            print("saved user done")
        return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['Employee_Name', 'Email', 'Department', 'Designation', 'Salary', 'Card_status', 'Profile_picture']

        widgets = {
            'Employee_Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'Department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department'}),
            'Designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation'}),
            'Salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary'}),
            'Card_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business card status'}),
            'Profile_picture': forms.FileInput(
                attrs={'class': 'form-control', 'placeholder': 'select profile picture'}),

        }


class LeaveConfForm(forms.ModelForm):
    class Meta:
        model = LeaveConf
        fields = ['Approve', ]

        widgets = {
            'Approve': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Message from HR Admin **optional**'}),
        }


class EmpNotifyForm(forms.ModelForm):
    class Meta:
        model = Notify
        fields = ['Notification_Subject', 'Notification', 'Department']

        widgets = {
            # 'Date' : forms.DateInput(attrs={'class':'form-control','placeholder': 'Email'}),
            'Notification_Subject': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter notification subject'}),
            'Notification': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write notice'}),
            'Department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write notice'}),

        }
