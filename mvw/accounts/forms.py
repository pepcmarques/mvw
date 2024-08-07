# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.utils.translation import gettext_lazy

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, help_text='username required')
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50, help_text='username required')
    email = forms.EmailField(max_length=200, help_text='email required')

    class Meta:
        model = User
        fields = ('username', 'email',)


class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField(
        label=gettext_lazy('Email'),
        widget=forms.TextInput(attrs={'class': 'span3'}))


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'Username', 'email': 'e-mail'}


class UsersUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        labels = {
            'username': 'Username',
            'first_name': 'First name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True


class PasswordChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PasswordChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
